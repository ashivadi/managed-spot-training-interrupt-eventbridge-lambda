# managed-spot-training-interrupt-eventbridge-lambda
This lambda is triggered by AWS Eventbridge when a Managed Spot Training Job is interrupted. Data Scientists and ML engineers who run training jobs overni    ght who don't want to deal with time delays due to spot interruptions can benefit. Additionally, this way, all jobs, time sensitive or not, can start with spot, and if needed piggy back on on-demand to realize cost benefits 

Use of [Training job state change](https://docs.aws.amazon.com/sagemaker/latest/dg/automating-sagemaker-with-eventbridge.html).
