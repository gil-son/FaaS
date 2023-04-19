import json
import boto3
from botocore.exceptions import ClientError

dynamo = boto3.resource("dynamodb").Table("Product")

def lambda_handler(event, context):
    body = None
    status_code = 200
    try:
        http_method = event['requestContext']['http']['method']
        path = event['requestContext']['http']['path']
        
        if http_method == "GET" and path == "/items":
            try:
                response = dynamo.scan()
                body = response['Items']
            except ClientError as e:
                error_message = e.response['Error']['Message']
                body = {"error": f"Failed to scan DynamoDB table: {error_message}"}
                status_code = 500
                
        elif http_method == "POST" and path == "/items":
            try:
                item = json.loads(event['body'])
                response = dynamo.put_item(Item=item)
                body = {"message": "Item added successfully"}
            except Exception as e:
                error_message = str(e)
                body = {"error": f"Failed to add item: {error_message}"}
                status_code = 500
                
        elif http_method == "GET" and path.startswith("/items/"):
            item_id = path.split("/")[2]
            try:
                response = dynamo.get_item(Key={"id": item_id})
                if "Item" in response:
                    body = response['Item']
                else:
                    body = {"error": "Item not found"}
                    status_code = 404
            except ClientError as e:
                error_message = e.response['Error']['Message']
                body = {"error": f"Failed to get item: {error_message}"}
                status_code = 500
                
        elif http_method == "PUT" and path.startswith("/items/"):
            item_id = path.split("/")[2]
            try:
                item = json.loads(event['body'])
                response = dynamo.update_item(
                    Key={"id": item_id},
                    UpdateExpression="SET #attr1 = :val1, #attr2 = :val2",
                    ExpressionAttributeNames={
                        "#attr1": "name",
                        "#attr2": "price"
                    },
                    ExpressionAttributeValues={
                        ":val1": item.get("name"),
                        ":val2": item.get("price")
                    },
                    ReturnValues="UPDATED_NEW"
                )
                body = {"message": "Item updated successfully"}
            except Exception as e:
                error_message = str(e)
                body = {"error": f"Failed to update item: {error_message}"}
                status_code = 500
                
        elif http_method == "DELETE" and path.startswith("/items/"):
            item_id = path.split("/")[2]
            try:
                response = dynamo.delete_item(Key={"id": item_id})
                body = {"message": "Item deleted successfully"}
            except ClientError as e:
                error_message = e.response['Error']['Message']
                body = {"error": f"Failed to delete item: {error_message}"}
                status_code = 500
                
        else:
            body = {"error": "Invalid request path or method"}
            status_code = 400
    
    except KeyError:
        http_method = 'unknown'
        path = 'unknown'
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    return body
