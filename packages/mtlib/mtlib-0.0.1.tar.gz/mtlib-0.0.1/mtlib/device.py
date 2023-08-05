
import asyncio
import aiocoap
import logging
import json
import socket
from threading import Thread

from .exceptions import *
#from .exception import MTException



class Device(object):
    def __init__(self,host):
        self.host = host
        self._observation = None

        self.logger = logging.getLogger(__name__)


    ########################################################################################
    #
    # Async Methods
    #
    ########################################################################################
    

    async def async_get_state(self):
        """Gets current state of device asynchronously
        
        Returns:
            string: The state (i.e. "ON", "OFF", "OPEN" or "CLOSED")

        Raises:
            mtlib.exceptions.MTException
        """
        uri = "coap://{}/state.json".format(self.host)
        result = await self._coap_get(uri)

        #Config the  request was successfull
        if not result.code.is_successful():
            raise ResponseError("COAP response Code: {}, Payoad:{}".format(result.code,result.payload))

        #Parse the json data
        try:
            data = json.loads(result.payload.decode("utf-8"))
        except json.decoder.JSONDecodeError as error:
            raise ResponseError("Invalid state data.  JSON Error decoding: {}".format(result.payload))

        #Make sure state is in the data
        if "state" not in data:
            raise ResponseError("Invalid response - Does not contain 'state' key: {}".format(data))

        return data["state"]

    
    async def async_get_info(self):
        """Retrieves a dict of info about the device asynchronously
        
        Returns:
            dict: Information about the devide.  Includes deviceName, model, serial.
                Other attributes may be included depending on the device.
        
        Raises: 
            mtlib.exceptions.MTException
        """
        uri = "coap://{}/info.json".format(self.host)
        result = await self._coap_get(uri)

        #Confirm the  request was successfull
        if not result.code.is_successful():
            raise  ResponseError("COAP response Code: {}, Payoad:{}".format(result.code,result.payload))

        #Parse the json data
        try:
            data = json.loads(result.payload.decode("utf-8"))
        except json.decoder.JSONDecodeError as error:
            raise ResponseError("Invalid state data.  JSON Error decoding: {}".format(result.payload))

        #All is good, return the info dict
        return data


    async def async_send_command(self, command):
        """Sends a command to the device asynchronously

        Args:
            command (string): The command to send.  (i.e. "ON", "OFF", "OPEN" or "CLOSE")

        Returns: 
            bool: True on success
        
        Raises:
            mtlib.exceptions.MTException
        """
        uri = "coap://{}/command".format(self.host)
        result = await self._coap_post(uri,payload=command)

        #Confirm the  request was successfull
        if not result.code.is_successful():
            raise  ResponseError("COAP response Code: {}, Payoad:{}".format(result.code,result.payload))

        return True

    async def async_on(self):
        """Sends "ON" command to the device asynchronously

        Returns: 
            bool: True on success
        
        Raises:
            mtlib.exceptions.MTException
        """
        return await self.async_send_command("ON")
    

    async def async_off(self):
        """Sends "OFF" command to the device asynchronously

        Returns: 
            bool: True on success
        
        Raises:
            mtlib.exceptions.MTException
        """
        return await self.async_send_command("OFF")


    async def async_toggle(self):
        """Sends "TOGGLE" command to the device asynchronously

        Returns: 
            bool: True on success
        
        Raises:
            mtlib.exceptions.MTException
        """
        return await self.async_send_command("TOGGLE")


    async def async_observe_state(self, callback):
        """Initiates observation of the state

        Callback is called whenever the state of the device changes

        Args:
            callback (callable): callback function to receive state changes
                Callback Args:
                    state (strinig) - The new device state

        Returns:
            boot: True on success

        Raises:
            mtlib.exceptions.MTException
        """

        # Inline callback method that reformats the Coap messages to just the state string
        def cb (message):
            data = json.loads( message.payload.decode( "utf-8" ) )
            callback( data["state"] )

        #Initiate the  observation
        uri = "coap://{}/state.json".format(self.host)
        obs = await self._coap_observe(uri)

        #Save reference to observation
        self._observation = obs

        #Register the callback
        self._observation.register_callback(cb)

        #Return true on success
        return True

    def cancel_observe_state(self):
        """ Cancels observation """

        self.logger.debug("Starting cancel_observe_state")
        if self._observation is not None:
            self.logger.debug("canceling state")
            self._observation.cancel()
            self.logger.debug("state canceled")
            self._observation = None




    ########################################################################################
    #
    # Private Methods
    #
    ########################################################################################

    async def _coap_get(self, uri):
        """Initiate a COAP GET request
        
        Args:
            uri (string): URI of the resource to get
        
        Returns:
            aiocoap.message.Message: Coap message

        Raises:
            mtlib.exceptions.MTException
        """
        result = await self._coap_request(uri, aiocoap.GET)
        return result


    async def _coap_post(self, uri, payload):
        """Initite a COAP POST request
        
        Args:
            uri (string): URI of the resource to get
            payload (string): Data to send in the post
        
        Returns:
            aiocoap.message.Message: Coap message

        Raises:
            mtlib.exceptions.MTException
        """
        result = await self._coap_request(uri, aiocoap.POST, payload)
        return result



    async def _coap_request(self, uri, method, payload=""):
        """Performs a coap Request
                
        Args:
            uri (string): URI of the resource to get
            method (aiocoap.numbers.codes.Code): coap Request code 
            payload (string): Data to send in the post
        
        Returns:
            aiocoap.message.Message: Coap message

        Raises:
            mtlib.exceptions.MTException

        """
        self.logger.debug("Starting '{}' request to {}".format(method,uri))

        #create the coap client context
        protocol = await aiocoap.Context.create_client_context()

        #create the request
        request = aiocoap.Message(code=method, uri=uri, payload=payload.encode() )

        #Send the COAP Message
        try:
            result = await protocol.request(request).response
            return result
        except aiocoap.error.RequestTimedOut as error:
            raise CoapRequestTimedOut("Connecting to {}".format(uri)) from error
        except socket.gaierror as error:
            raise NameNotResolved("Connecting to {}".format(uri)) from error
        except OSError as error:
            if error.errno == 113:
                raise NoRouteToHost("Connecting to {}".format(uri)) from error
            elif error.errno == 111:
                raise ConnectionRefused("Connecting to {}".format(uri)) from error
            else:
                raise error            

    async def _coap_observe(self, uri):
        """
        Innitiates a COAP observe request

        Args:
            uri (string): URI of the resource to observe
        
        Returns:
            aiocoap.protocol.ClientObservation: Observation object

        Raises:
            mtlib.exceptions.MTException

        """
        self.logger.debug("Starting 'Observe' of {}".format(uri))
        protocol = await aiocoap.Context.create_client_context()

        message = aiocoap.Message(code=aiocoap.GET,uri=uri, observe=0)

        request = protocol.request(message)

        #Gather the results
        results = await asyncio.gather(
            request.response, return_exceptions=True
        )
        #Loop through he responses - there should only be one
        assert len(results) == 1
        result = results[0]

        if isinstance(result, Exception):
            return MTException("COAP exception",result)
        elif not hasattr(result.opt,"observe") or result.opt.observe == None:
            return MTException("Resource at {} is not observable".format(uri) )
        else:
            return request.observation


# # OLD METHODS

#     async def xxasync_observe_state(self, callback):
        
#         # This callback resives the additional observatio responses from  
#         # _coap_observe() confirms they are still good and calls the 
#         # callback  param
#         def cb (result):
#             #See if COAP returnd an error
#             if isinstance(result, Exception):
#                 callback(MTException("COAP exception",result) )

#             #Confirm the  request was successfull
#             if not result.code.is_successful():
#                 callback( MTException("COAP Error response Code: {}, Payoad:{}".format(result.code,result.payload)) )

#             #Parse the json data
#             try:
#                 data = json.loads(result.payload.decode("utf-8"))
#             except json.decoder.JSONDecodeError as error:
#                 callback ( MTException("Invalid state data.  JSON Error decoding: {}".format(result.payload)) )

#             #Make sure state is in the data
#             if "state" not in data:
#                 callback ( MTException("Invalid response - Does not contain state key: {}".format(data)) )
            
#             #All is good, callback with the state
#             return callback(data["state"])

#         uri = "coap://{}/state.json".format(self.host)
#         result = await self._coap_observe(uri, cb)

#         #See if COAP returnd an error
#         if isinstance(result, Exception):
#             return MTException("COAP exception",result)

#         #Confirm the  request was successfull
#         if not result.code.is_successful():
#             return MTException("COAP Error response Code: {}, Payoad:{}".format(result.code,result.payload))

#         #Parse the json data
#         try:
#             data = json.loads(result.payload.decode("utf-8"))
#         except json.decoder.JSONDecodeError as error:
#             return MTException("Invalid state data.  JSON Error decoding: {}".format(result.payload))

#         #Make sure state is in the data
#         if "state" not in data:
#             return MTException("Invalid response - Does not contain state key: {}".format(data))

#         #All is good, return the state
#         return data["state"]





#     async def xx_coap_observe(self, uri, callback):
#         """
#         Innitiates a COAP observe request
#         """
#         self.logger.debug("Starting 'Observe' of {}".format(uri))
#         protocol = await aiocoap.Context.create_client_context()

#         message = aiocoap.Message(code=aiocoap.GET,uri=uri, observe=0)

#         request = protocol.request(message)

#         #Gather the results
#         results = await asyncio.gather(
#             request.response, return_exceptions=True
#         )
#         #Loop through he responses - there should only be one
#         assert len(results) == 1
#         message = results[0]

#         if isinstance(message, Exception):
#             #Its an error, return it
#             return message
#         else:
#             #Save reference to observation object
#             self._observation = request.observation

#             callback(message)

#             async for message in self._observation:
#                 callback(message)


    ########################################################################################
    #
    # Sync Methods
    #
    ########################################################################################


    def get_state(self):
        """
        Retrieves the current state of the device
        Synchronous version of async_get_state()

        @returns: string (i.e. "ON", "OFF", "OPEN" or "CLOSED") 
        @raises: MTException on errors
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete( self.async_get_state() )
        
        if isinstance(result,MTException):
            raise result
        else:
            return result

    def get_info(self):
        """
        Retrieves a dict of info about the device.
        Synchronous version of async_get_info()
    
        @returns: dict - include deviceName, model, serial.  Other attributes may be included depending on the device.
        @raises: MTException 
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete( self.async_get_info() )
        
        if isinstance(result,MTException):
            raise result
        else:
            return result

    def send_command(self,command):
        """
        Sends a command to the device.
        Synchronous version of async_send_command()

        @param command: string - The command to send.  (i.e. "ON", "OFF", "OPEN" or "CLOSE")
        @returns: True on success
        @raises: MTException 
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete( self.async_send_command(command) )
        
        if isinstance(result,MTException):
            raise result
        else:
            return result

    def on(self):
        """
        Sends command "ON" to device
        """
        return self.send_command("ON")

    def off(self):
        """
        Sends command "OFF" to device
        """
        return self.send_command("OFF")

    def toggle(self):
        """
        Sends command TOGGLE to device
        """
        return self.send_command("TOGGLE")


    def observe_state(self, callback):
        """
        Observes the current state of the device
        Synchronous version of async_get_state()

        @param: callable( state: string ) - Callback function.  When start on device changes the callback
               function is called with the new state
                           
        """

        def start_loop(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        loop = asyncio.new_event_loop()
        t = Thread(target=start_loop, args=(loop,))
        t.start()

        loop.call_soon_threadsafe(asyncio.async, self.async_observe_state(callback))

