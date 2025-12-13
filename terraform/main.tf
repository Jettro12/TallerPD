provider "aws" {
  region = "us-east-1"
}

# --- 1. DATOS (Buscar VPC y AMI automáticamente) ---
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Busca la última AMI de Amazon Linux 2023
data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

# --- 2. SECURITY GROUP (Permitir tráfico) ---
resource "aws_security_group" "web_sg" {
  name        = "examen_sg"
  description = "Permitir HTTP y SSH"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# --- 3. LOAD BALANCER (ALB) ---
resource "aws_lb" "mi_alb" {
  name               = "examen-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web_sg.id]
  subnets            = data.aws_subnets.default.ids
}

resource "aws_lb_target_group" "mi_tg" {
  name     = "examen-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = data.aws_vpc.default.id
  health_check {
    path = "/"
    matcher = "200"
  }
}

resource "aws_lb_listener" "front_end" {
  load_balancer_arn = aws_lb.mi_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.mi_tg.arn
  }
}

# --- 4. LAUNCH TEMPLATE (El cerebro con Docker) ---
resource "aws_launch_template" "mi_lt" {
  name_prefix   = "examen-lt-"
  image_id      = data.aws_ami.al2023.id
  instance_type = "t2.micro" # O t3.micro si prefieres

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.web_sg.id]
  }

  # Script User Data codificado en Base64
  user_data = base64encode(<<-EOF
    #!/bin/bash
    yum update -y
    yum install -y docker
    systemctl start docker
    systemctl enable docker
    usermod -a -G docker ec2-user
    # Limpieza preventiva
    docker rm -f $(docker ps -a -q) || true
    # Descargar tu imagen de GitHub Actions
    docker pull stoicpath/backend_helloworld:latest
    # Correr contenedor
    docker run -d --restart always -p 80:80 stoicpath/backend_helloworld:latest
  EOF
  )
}

# --- 5. AUTO SCALING GROUP (3 a 7 instancias) ---
resource "aws_autoscaling_group" "mi_asg" {
  name                = "examen-asg"
  desired_capacity    = 3
  max_size            = 7
  min_size            = 3
  vpc_zone_identifier = data.aws_subnets.default.ids
  target_group_arns   = [aws_lb_target_group.mi_tg.arn]

  launch_template {
    id      = aws_launch_template.mi_lt.id
    version = "$Latest"
  }
  
  # Importante para que refresque instancias si cambias el template
  instance_refresh {
    strategy = "Rolling"
  }
}

# --- 6. REGLA DE ESCALADO (Tráfico de Red / Network) ---
resource "aws_autoscaling_policy" "network_policy" {
  name                   = "escalar-por-red"
  autoscaling_group_name = aws_autoscaling_group.mi_asg.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageNetworkIn" # Tráfico de red entrante
    }
    target_value = 1000000.0 # Escalar si el tráfico supera ~1MB (Ejemplo para prueba)
  }
}