from typing import Dict, Any

def get_customer_info(customer_id: str) -> Dict[str, Any]:
    """
    Simulates a CRM lookup for customer information.
    
    Args:
        customer_id (str): The unique identifier for the customer.
        
    Returns:
        dict: Customer details including name, email, and account status.
    """
    # Mock database
    customers = {
        "CUST-001": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "account_status": "Active",
            "last_interaction": "2024-03-15"
        },
        "CUST-002": {
            "name": "Jane Smith",
            "email": "jane.smith@enterprise.org",
            "account_status": "Premium",
            "last_interaction": "2024-04-01"
        }
    }
    
    return customers.get(customer_id, {"error": "Customer not found"})
