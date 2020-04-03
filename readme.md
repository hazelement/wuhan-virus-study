# Wuhan virus modeling

This project is deployed to AWS Lambda using cloudformation. The lambda function is triggered everyday to replot the graph. New graphs are saved to S3 bucket. All AWS infrastructure and policies are specified in `template.yaml`. 

refer to https://www.zhihu.com/question/367466399 for model formula

## Using si_model

Country incremental
![alt text](https://harry-lambda-projects.s3-us-west-2.amazonaws.com/covid19/country_incrementals.png)

Country accumulative
![alt text](https://harry-lambda-projects.s3-us-west-2.amazonaws.com/covid19/country_totals.png)

### Countries
Canada
![alt text](plots/Canada.png)

US
![alt text](plots/United States.png)




### Compare to SARS
Need more data for wuhan
![alt text](plots/wuhan.png)

Compare to SARS
![alt text](plots/sars.png)

### Todo

[ ] SIR model analysis
