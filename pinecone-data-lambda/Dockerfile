FROM amazon/aws-lambda-python:3.9
# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
 
# Copy function code
COPY update_data.py ${LAMBDA_TASK_ROOT}
# Use Secrets Manager
COPY credentials.json ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "update_data.main" ] 