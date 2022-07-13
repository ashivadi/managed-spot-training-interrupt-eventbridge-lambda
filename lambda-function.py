import boto3


def lambda_handler(event, context):
    if (event["detail"]['SecondaryStatus'] == 'Interrupted'): # and
            # event["Tags"]['restartWithOnDemandFlag'] == 'True'):

        training_job_name = event["detail"]['TrainingJobName']
        sm = boto3.client('sagemaker')
        job = sm.describe_training_job(TrainingJobName=training_job_name)

        # Clone details to new job
        training_job_suffix = '-RESTARTED-OnDemand'
        training_job_name_new = training_job_name + training_job_suffix

        print("Starting training job %s" % training_job_name_new)
        
        StoppingConditionNew = {}
        StoppingConditionNew['MaxRuntimeInSeconds'] = job['StoppingCondition']['MaxRuntimeInSeconds']
        
        resp = sm.create_training_job(
            TrainingJobName=training_job_name_new,
            AlgorithmSpecification=event["detail"]['AlgorithmSpecification'],
            HyperParameters=job['HyperParameters'] if 'HyperParameters' in job else None,
            OutputDataConfig=job['OutputDataConfig'],
            RoleArn=job['RoleArn'],
            InputDataConfig=job['InputDataConfig'] if 'InputDataConfig' in job else None,
            ResourceConfig=job['ResourceConfig'],
            StoppingCondition=StoppingConditionNew,
            CheckpointConfig=job['CheckpointConfig'],
            EnableManagedSpotTraining=False,
            Tags=event["detail"]["Tags"] if 'Tags' in event else [],
            EnableNetworkIsolation=job['EnableNetworkIsolation'] if 'EnableNetworkIsolation' in job else False,
            EnableInterContainerTrafficEncryption=job['EnableInterContainerTrafficEncryption'] if 'EnableInterContainerTrafficEncryption' in job else False,
            ProfilerConfig=job['ProfilerConfig'] if 'ProfilerConfig' in job else None,
            ProfilerRuleConfigurations=job['ProfilerRuleConfigurations'] if 'ProfilerRuleConfigurations' in job else None,
        )
            
                
        print(resp)

        # Stop the old job
        print("Stopping old spot training job %s" % event["detail"]['TrainingJobName'])
        
        resp = sm.stop_training_job(TrainingJobName=event["detail"]['TrainingJobName'])
        print(resp)
