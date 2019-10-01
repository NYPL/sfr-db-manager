################################################################################
#                                                                              #
# Terraform Configuration for sfr-db-manager Lambda Function                   #
# NOTE: This is not intended to be run as a standalone .tf. It should be       #
# included as a module in a pipeline deployment process                        #
#                                                                              #
################################################################################

resource "local_file" "func_build" {
    filename                = "${var.out_file}"
    provisioner "local-exec" {
        command             = "./func-build.sh ${path.module} ${var.environment}"
    }
}

data "external" "zipHash" {
    program = ["./getZipHash.sh", "${var.out_file}"]

    depends_on              = [local_file.func_build]
}

resource "aws_lambda_function" "sfr-db-manager" {
    filename                = "${var.out_file}"
    source_code_hash        = "${data.external.zipHash.result["ziphash"]}"
    function_name           = "sfr-db-manager-development"
    handler                 = "service.handler"
    description             = "Managers updates to SFR database"
    runtime                 = "python3.7"
    role                    = "lambda_basic_execution"
    memory_size             = 192
    timeout                 = 180
    
    vpc_config {
        subnet_ids          = ["subnet-12aa8a65"]
        security_group_ids  = ["sg-5521ef32"]
    }

    environment {
        variables = {
            ENV             = "${var.environment}"
            LOG_LEVEL       = "${var.log_level}"
            DB_HOST         = "${var.db_host_encoded}"
            DB_PORT         = "${var.db_port}"
        }
    } 

    provisioner "local-exec" {
        command             = "rm builtSource.zip"
    }

    depends_on              = [data.external.zipHash]
}
