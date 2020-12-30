"""
 Copyright (C) 2020 Dabble Lab - All Rights Reserved
 You may use, distribute and modify this code under the
 terms and conditions defined in file 'LICENSE.txt', which
 is part of this source code package.
 
 For additional copyright information please
 visit : http://dabblelab.com/copyright
 """

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.dispatch_components import (AbstractRequestHandler, AbstractExceptionHandler, AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_model.ui import AskForPermissionsConsentCard

import logging
import json
import random

# Initializing the logger and setting the level to "INFO"
# Read more about it here https://www.loggly.com/ultimate-guide/python-logging-basics/
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

FULL_NAME_PERMISSION = ["alexa::profile:name:read"]
EMAIL_PERMISSION = ["alexa::profile:email:read"]
MOBILE_PERMISSION = ["alexa::profile:mobile_number:read"]

# Intent Handlers

#This Handler is called when the skill is invoked by using only the invocation name(Ex. Alexa, open template six)
class LaunchRequestHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        skill_name = language_prompts["SKILL_NAME"]
        
        speech_output = random.choice(language_prompts["WELCOME"]).format(skill_name)
        reprompt = random.choice(language_prompts["WELCOME_REPROMPT"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

# This handler fetches the users address and speaks it back. In case the address is invalid
# or the user has not provided required permissions, it guides the user to do the needful.
class NameIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("NameIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        try:
            ups_service_client = handler_input.service_client_factory.get_ups_service()
            profile_name = ups_service_client.get_profile_name()

            if profile_name is None:
                handler_input.response_builder.speak(language_prompts["NO_NAME"])
            else:
                handler_input.response_builder.speak(language_prompts["TELL_NAME"].format(profile_name))
                handler_input.response_builder.ask(language_prompts["REPROMPT"])
            return handler_input.response_builder.response
        
        except:
            return (
                    handler_input.response_builder
                        .speak(language_prompts["NOTIFY_MISSING_PERMISSIONS"])
                        .set_card(AskForPermissionsConsentCard(permissions=FULL_NAME_PERMISSION))
                        .response
                    )

class EmailIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("EmailIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        try:
            ups_service_client = handler_input.service_client_factory.get_ups_service()
            profile_email = ups_service_client.get_profile_email()

            if profile_email is None:
                handler_input.response_builder.speak(language_prompts["NO_EMAIL"])
            else:
                handler_input.response_builder.speak(language_prompts["TELL_EMAIL"].format(profile_email))
                handler_input.response_builder.ask(language_prompts["REPROMPT"])
            return handler_input.response_builder.response
        
        except:
            return (
                    handler_input.response_builder
                        .speak(language_prompts["NOTIFY_MISSING_PERMISSIONS"])
                        .set_card(AskForPermissionsConsentCard(permissions=EMAIL_PERMISSION))
                        .response
                    )

class MobileIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("MobileIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        try:
            ups_service_client = handler_input.service_client_factory.get_ups_service()
            profile_mobile = ups_service_client.get_profile_mobile_number()

            if profile_mobile is None:
                handler_input.response_builder.speak(language_prompts["NO_MOBILE"])
            else:
                handler_input.response_builder.speak(language_prompts["TELL_MOBILE"].format(profile_mobile.phone_number))
                handler_input.response_builder.ask(language_prompts["REPROMPT"])
            return handler_input.response_builder.response
        
        except:
            return (
                    handler_input.response_builder
                        .speak(language_prompts["NOTIFY_MISSING_PERMISSIONS"])
                        .set_card(AskForPermissionsConsentCard(permissions=MOBILE_PERMISSION))
                        .response
                    )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["CANCEL_STOP_RESPONSE"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .set_should_end_session(True)
                .response
            )

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["HELP"])
        reprompt = random.choice(language_prompts["HELP_REPROMPT"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

# This Handler handles utterances that can't be matched to any other intent handler.
class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["FALLBACK"])
        reprompt = random.choice(language_prompts["FALLBACK_REPROMPT"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class SessionEndedRequesthandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)
    
    def handle(self, handler_input):
        logger.info("Session ended with the reason: {}".format(handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response

# Exception Handlers

# This exception handler handles syntax or routing errors. If you receive an error stating 
# the request handler is not found, you have not implemented a handler for the intent or 
# included it in the skill builder below
class CatchAllExceptionHandler(AbstractExceptionHandler):
    
    def can_handle(self, handler_input, exception):
        return True
    
    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        speech_output = language_prompts["ERROR"]
        reprompt = language_prompts["ERROR_REPROMPT"]
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

# Interceptors

# This interceptor logs each request sent from Alexa to our endpoint.
class RequestLogger(AbstractRequestInterceptor):

    def process(self, handler_input):
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))

# This interceptor logs each response our endpoint sends back to Alexa.
class ResponseLogger(AbstractResponseInterceptor):

    def process(self, handler_input, response):
        logger.debug("Alexa Response: {}".format(response))

# This interceptor is used for supporting different languages and locales. It detects the users locale,
# loads the corresponding language prompts and sends them as a request attribute object to the handler functions.
class LocalizationInterceptor(AbstractRequestInterceptor):

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        
        try:
            with open("languages/"+str(locale)+".json") as language_data:
                language_prompts = json.load(language_data)
        except:
            with open("languages/"+ str(locale[:2]) +".json") as language_data:
                language_prompts = json.load(language_data)
        
        handler_input.attributes_manager.request_attributes["_"] = language_prompts

# Skill Builder
# Define a skill builder instance and add all the request handlers,
# exception handlers and interceptors to it.

sb = CustomSkillBuilder(api_client=DefaultApiClient())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(NameIntentHandler())
sb.add_request_handler(EmailIntentHandler())
sb.add_request_handler(MobileIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequesthandler())

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

lambda_handler = sb.lambda_handler()