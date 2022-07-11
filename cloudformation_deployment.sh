aws cloudformation deploy --template-file C:/Users/User/Documents/team3/team-3-project/updated-cf-template.yml --stack-name realstackteam3 --s3-bucket cloudformation-ayub-test-bucket --region eu-west-1 --parameter-overrides NotificationBucket=delon6-team3-raw-data DeploymentBucket=cloudformation-ayub-test-bucket DeploymentPackageKey=src.zip --capabilities CAPABILITY_IAM


#zip up layers into the deploment bucket and provide filename instead of ziplayer.zip

#deployment bucket--> cloudformation-ayub-test-bucket, where the templates and zips are stored
#notification bucket--> csv-test-ayub, this where my csvs are landing ie jakub bucket
# NotificationBucket=awaynepython DeploymentBucket=team-4-zip-temp-bucket DeploymentPackageKey=my-deployment-package.zip --capabilities CAPABILITY_IAM





