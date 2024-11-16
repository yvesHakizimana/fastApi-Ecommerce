from fastapi import HTTPException


class ResponseHandler:
    @staticmethod
    def success(message, data=None):
        return {'message': message, 'data': data}

    @staticmethod
    def get_single_success(entity_name, id, data):
        message = f"Details for {entity_name} with id {id}"
        return ResponseHandler.success(message, data)

    @staticmethod
    def create_success(entity_name, id,  data):
        message = f"{entity_name} with id  {id} was created successfully"
        return ResponseHandler.success(message, data)

    @staticmethod
    def update_success(entity_name, id, data):
        message = f"{entity_name} with id {id} was updated successfully"
        return ResponseHandler.success(message, data)

    @staticmethod
    def delete_success(entity_name, id, data):
        message = f"{entity_name} with id  {id} was deleted successfully"
        return ResponseHandler.success(message, data)

    @staticmethod
    def not_found_error(entity_name="", id=None):
        message = f"{entity_name} with {id} was not found!"
        raise HTTPException(status_code=404, detail=message)

    @staticmethod
    def auth_bad_request_error():
        message = f"Incorrect username or password"
        raise HTTPException(status_code=400, detail=message, headers={"WWW-Authenticate": "Bearer"})

    @staticmethod
    def invalid_token(entity_name=""):
        raise HTTPException(status_code=401, detail=f"Invalid {entity_name} token", headers={"WWW-Authenticate": "Bearer"},)


