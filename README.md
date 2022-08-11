# Intro
A quick'n'dirty exploration of [Lambda Authorisers for Amazon API Gateway HTTP APIs](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html "Lambda Authorisers for API Gateway HTTP API")

# WARNING!
This is all utterly ridiculous in its approach to security, it is for exploration only! 🖖

# Testing
I've done some. But not much, like creating then deleting resources and creating them again (although see [Log Groups](#log-groups) 🗑) and there have been hiccups deleting due to seemingly circular dependencies, deleting again whilst not retaining resources seems to work fine...

# Behaviour  
Simply, the API Gateway is configured expect a header (`Authorization`) containing an authorisation value, if it is missing, expect a `401`, but if the correct header is present, it is passed to the [authoriser](./authoriser/lambda_function.py) function, which validates the value and returns an outcome. If the request is authorised, the [backend](./backend/lambda_function.py) function is [invoked](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html "API Gateway Integration") and returns the entire `event` object (see [AWS documentation](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html "AWS docs")) which is stupidly insecure, but definitely handy for testing. If the request is not authorised, a `403` is returned.

## Obligatory Diagram 
![Architecture](./Lambda%20Authoriser.png "Trivial AWS architecture, and apologies if you are viewing this in dark mode!")

# Creation
```bash
STACK_NAME=APIGatewayHTTPAPIWithLambdaAuthoriser
echo "To override parameters, add --parameters ParameterKey=KEY,ParameterValue=VALUE to the create-stack" > /dev/null
aws cloudformation create-stack --stack-name ${STACK_NAME} --template-body file://lambda_authoriser.yml --capabilities CAPABILITY_NAMED_IAM --no-cli-pager
aws cloudformation wait stack-create-complete --stack-name ${STACK_NAME}
```

Note that this was written whilst supping Jack Daniels one evening, hence the code for the two Lambda functions are embedded in the template... I make no apologies for the readability squint that may require 🥃

Also, `--capabilities CAPABILITY_NAMED_IAM`, again, no apologies, I liked named IAM roles and polices, what can I say? 😏

## Log Groups
The Log Groups are set to `Retain` to prevent logging data vanishing if the stack is deleted, but this does present a problem (which I'm sure has an elegant solution) when creating the stack after a deletion, because the resource is still there, so, adjust the following if you modify the API and/or function names, but this might be handy:
```bash
for log_group in /api/LambdaAuthoriser/test /aws/lambda/authoriser /aws/lambda/backend; do
  aws logs delete-log-group --log-group-name ${log_group}
done
```

# Usage
For testing, `curl` is nice and easy...

## Happy Path 👌
```bash
URL=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query "Stacks[?StackName=='APIGatewayHTTPAPIWithLambdaAuthoriser'][].Outputs[?OutputKey=='URL'].OutputValue" --output text --no-cli-pager)
curl -H "Authorization: correct-horse:battery/staple" ${URL}
```

## 401 🤦‍♂️
```bash
URL=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query "Stacks[?StackName=='APIGatewayHTTPAPIWithLambdaAuthoriser'][].Outputs[?OutputKey=='URL'].OutputValue" --output text --no-cli-pager)
curl ${URL}
```

## 403 ⛔️
```bash
URL=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query "Stacks[?StackName=='APIGatewayHTTPAPIWithLambdaAuthoriser'][].Outputs[?OutputKey=='URL'].OutputValue" --output text --no-cli-pager)
curl -H "Authorization: wrong-aardvark:capacitor/nail" ${URL}
```

## Pot Luck ☘️
```bash
URL=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query "Stacks[?StackName=='APIGatewayHTTPAPIWithLambdaAuthoriser'][].Outputs[?OutputKey=='URL'].OutputValue" --output text --no-cli-pager)
curl -H "Authorization: random-horse:battery/staple" ${URL}
```

# Reminder
DO NOT USE THIS NONSENSE FOR ANYTHING OTHER THAN LEARNING! 🔓