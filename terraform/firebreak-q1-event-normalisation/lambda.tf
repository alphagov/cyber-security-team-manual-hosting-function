# Lambda

data "archive_file" "firebreakq1faas_zip" {
  type        = "zip"
  source_dir  = "../../"
  output_path = "../../firebreakq1faas.zip"
}

resource "aws_lambda_function" "firebreakq1faas" {
  filename         = "${data.archive_file.firebreakq1faas_zip.output_path}"
  source_code_hash = "${data.archive_file.firebreakq1faas_zip.output_base64sha256}"
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
