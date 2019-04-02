# Lambda
resource "aws_lambda_function" "firebreakq1faas" {
  filename         = "../../firebreakq1faas.zip"
  source_code_hash = "${filebase64sha256("../../firebreakq1faas.zip")}"
  function_name    = "firebreakq1faas"
  role             = "${aws_iam_role.firebreakq1faas_iam_lambda.arn}"
  handler          = "lambda_handler.lambda_handler"
  runtime          = "${var.runtime}"

  #  environment = {
  #    variables = {
  #      VAR1       = "${var.1}"
  #      VAR2       = "${var.2}"
  #    }
  #  }
  vpc_config {
    subnet_ids = ["${aws_subnet.alb-frontend-subnet1-AZ-A.id}", "${aws_subnet.alb-frontend-subnet2-AZ-B.id}"]
    security_group_ids = ["${aws_security_group.event-normalisation-lambda-ingress.id}", "${aws_security_group.event-normalisation-lambda-egress.id}"]
  }

#  environment = {
#    variables = {
#      VAR1       = "${var.1}"
#      VAR2       = "${var.2}"
#    }
#  }
}

resource "aws_iam_role" "firebreakq1faas_iam_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda-policy-attach" {
  role       = "${aws_iam_role.firebreakq1faas_iam_lambda.name}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_role_policy" "firebreakq1faas_iam_lambda" {
  name = "test_policy"
  role = "${aws_iam_role.firebreakq1faas_iam_lambda.id}"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:eu-west-2:${data.aws_caller_identity.current.account_id}:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:eu-west-2:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/firebreakq1faas:*"
            ]
        }
    ]
}
EOF
}

resource "aws_lambda_permission" "with_lb" {
  statement_id  = "AllowExecutionFromlb"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.firebreakq1faas.arn}"
  principal     = "elasticloadbalancing.amazonaws.com"
  source_arn    = "${aws_lb_target_group.event-normalisation-tg.arn}"
}

resource "aws_lb_target_group_attachment" "firebreakq1faas" {
  target_group_arn = "${aws_lb_target_group.event-normalisation-tg.arn}"
  target_id        = "${aws_lambda_function.firebreakq1faas.arn}"
  depends_on       = ["aws_lambda_permission.with_lb"]
}
