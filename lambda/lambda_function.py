"""
AWS Lambda Function Entry Point for BEA Pumpkin Pi
==================================================

Main entry point for the BEA Pumpkin Pi Alexa skill.
Handles all Alexa requests and routes them to appropriate handlers.

© 2025 Jeremy F. Jackson dba BEATEK. All Rights Reserved.
"""

import logging
import json
from intent_handlers import lambda_handler

# Configure logging for Lambda
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """
    AWS Lambda entry point for BEA Pumpkin Pi Alexa Skill
    
    Args:
        event: Alexa request event
        context: Lambda context object
        
    Returns:
        Alexa response
    """
    logger.info("BEA Pumpkin Pi skill invoked")
    logger.debug(f"Event: {json.dumps(event, indent=2)}")
    
    try:
        # Use the Alexa Skills Kit handler
        response = lambda_handler(event, context)
        
        logger.info("BEA Pumpkin Pi response generated successfully")
        logger.debug(f"Response: {json.dumps(response, indent=2)}")
        
        return response
        
    except Exception as e:
        logger.error(f"BEA Pumpkin Pi error: {str(e)}")
        
        # Return error response
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Sorry, I'm experiencing technical difficulties. Please try again later."
                },
                "shouldEndSession": True
            }
        }