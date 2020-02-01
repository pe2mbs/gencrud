# -*- coding: utf-8 -*-
#
# Angular base module, containing the app factory function.
# Copyright (C) 2018 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
import logging
from typing import Callable, Tuple
import stomp

__version__ = "0.1.0"

# Init logger a default logger
logger = logging.getLogger( 'webapp.stomp' )

class StompCallback( object ):
    def __init__( self, cb, **kwargs ):
        self.__cb = cb
        self.__filterArgs = kwargs
        return
    
    def __call__( self, args, kwargs ):
        logger.debug( "StompCallback.__call__( {1}, {2} )".format( self.__cb, args, kwargs ) )
        if len( self.__filterArgs ) == 0:
            return self.__cb( *args, **kwargs )
        
        logger.debug( "{0}( {1}, {2} ) => filterArgs {3}".format( self.__cb, args, kwargs, self.__filterArgs ) )
        headers = args[0]
        for key, value in self.__filterArgs.items():
            compare = headers[ key ] == value
            logger.debug( "{0} := {1} == ({3}) {2} ".format( key, value, headers[ key ], compare ) )
            if compare:
                logger.debug( "call {0}( {1} )".format( self.__cb, args ) )
                return self.__cb( *args, **kwargs )
               
        return None 

    @property
    def subscription( self ):
        return self.__filterArgs
    

class StompCallbackList( object ):
    def __init__( self ):
        self.__cbList = [] 
        return
    
    def append( self, cb, **kwargs ):
        self.__cbList.append( StompCallback( cb, **kwargs ) )
        return

    def set( self, cb, **kwargs ):
        self.__cbList = [ StompCallback( cb, **kwargs ) ]
        return
    
    def __call__( self, *args, **kwargs ):
        result = None
        args = list( args )
        for cb in self.__cbList:
            logger.debug( "from StompCallbackList::{0}( {1}, {2} )".format( cb, args, kwargs ) )
            result = cb( args, kwargs )
            if result is not None:
                if type( result ) in ( list, tuple ) and len( result ) > 0:
                    for idx, value in enumerate( result ):
                        args[ idx ] = value
                        
                else:
                    args[ 0 ] = result
                               
        return result

    def getSubscriptions( self ):
        rList = []
        for item in self.__cbList:
            rList.append( item.subscription )
            
        return rList 
    

class FlaskStompListener( stomp.ConnectionListener ):
    def __init__( self ):
        # def __init__( self , broker, route_to_flask ):
        # private members
        #self.__app                      = route_to_flask
        #self.__broker                   = broker
        # protected members
        # Generic handlers
        self._onError                   = StompCallbackList()
        self._onConnecting              = StompCallbackList()
        self._onConnected               = StompCallbackList()
        self._onDisconnected            = StompCallbackList()
        self._onHeartbeat               = StompCallbackList()
        self._onHeartbeatTimeout        = StompCallbackList()
        self._onReceiverLoopCompleted   = StompCallbackList()
        # Message handlers
        self._onBeforeMessage           = StompCallbackList()
        self._onMessage                 = StompCallbackList()
        self._onSend                    = StompCallbackList()
        self._onReceipt                 = StompCallbackList()
        return

    """
        Generic callbacks
    """
    def on_receiver_loop_completed( self, headers, message ):
        """Calls the receiver loop completed callback
        
        :param headers: 
        :param message: 
        :rtype: None
        """
        logger.debug( 'on_receiver_loop_completed an error %s "%s"' % ( headers, message ) )
        self._onReceiverLoopCompleted( headers, message, **headers )
        return

    def on_error( self, headers, message ):
        """Calls the error callback
        
        :param headers: 
        :param message: 
        :rtype: None
        """
        logger.debug( 'received an error %s "%s"' % ( headers, message ) )
        self._onError( headers, message, **headers )
        return

    def on_connecting( self, host_and_port ):
        """Calls the connecting callback
        
        :param (str,int) host_and_port:
        :rtype: None
        """
        logger.debug( 'on_connecting %s %s' % host_and_port )
        self._onConnecting( host_and_port )
        return

    def on_connected( self, headers, message ):
        """Calls the connected callback
        
        :param dict headers:
        :param message:
        :rtype: None
        """
        logger.debug( 'on_connected %s %s' % ( headers, message ) )
        self._onConnected( headers, message, **headers )
        return

    def on_disconnected( self ):
        """Calls the disconnect callback
        
        :rtype: None
        """
        logger.info( 'on_disconnected' )
        self._onDisconnected()
        return

    def on_heartbeat( self ):
        """Calls the heartbeat callback
        
        :return: 
        """
        logger.debug( 'on_heartbeat' )
        self._onHeartbeat()
        return

    def on_heartbeat_timeout( self ):
        """Calls the heartbeat timeout callback
        
        :return: 
        """
        logger.debug( 'on_heartbeat_timeout' )
        self._onHeartbeatTimeout()
        return

    """
        Message callbacks
    """
    def on_before_message( self, headers, message ):
        """The callback for on before message 
        
        :param dict headers:
        :param message:
        """
        logger.debug('on_before_message %s "%s"' % ( headers, message ) )
        return self._onBeforeMessage( headers, message, **headers )

    def on_message( self, headers, message ):
        """The callback for on message 
        
        :param dict headers:
        :param message:
        """
        logger.debug( 'received a message %s "%s"' % ( headers, message ) )
        return self._onMessage( headers, message, **headers )
 

    def on_receipt( self, headers, message ):
        """The callback for on receipt 
        
        :param dict headers:
        :param message:
        """
        logger.debug( 'received a message "%s"' % message )
        return self._onReceipt( headers, message, **headers )
        

    def on_send( self, frame ):
        """The callback for on send 
        
        :param Frame frame:
        """
        logger.debug( 'on_send %s %s %s' % ( frame.cmd, frame.headers, frame.body ) )
        return self._onSend( frame, **frame.headers )
        

class FlaskStomp( object ):
    """Main Mqtt class."""

    def __init__( self, app = None ):
        # type: (Flask) -> None
        self.__app                  = None
        self.__connected            = False
        self.__username             = ''
        self.__password             = ''
        self.__broker               = None
        self.__onUnsubscribe        = StompCallbackList()
        self.__onSubscribe          = StompCallbackList()
        self.__listener             = FlaskStompListener()
        if app is not None:
            self.init_app( app )

        return

    def init_app( self, app ):
        """Init the Flask-Stomp addon.
        
        :param Flask app:
        """
        if not app.config.get( "STOMPMQ_ENABLED", False ):
            return

        self.__app          = app
        self.__username     = app.config.get( "STOMPMQ_USERNAME", "" )
        self.__password     = app.config.get( "STOMPMQ_PASSWORD", "" )
        version             = app.config.get( "STOMPMQ_VERSION", "1.1" )
        broker_hosts        = app.config.get( "STOMPMQ_BROKER_HOSTS", [] )
        if len( broker_hosts ) == 0:
            broker_hosts.append( [ app.config.get( "STOMPMQ_BROKER_URL", "localhost" ), 
                                   app.config.get( "STOMPMQ_BROKER_PORT", 61613 ) ] )
        global logger
        #logger = app.logger  
        logger.info( 'MQ username     : %s' % ( self.__username ) )
        logger.info( 'MQ password     : %s' % ( self.__password ) )
        logger.info( 'MQ version      : %s' % ( version ) )
        logger.info( 'MQ broker_hosts : %s' % ( repr( broker_hosts ) ) )

        if version == '1.0':
            self.__broker = stomp.Connection10( broker_hosts )

        elif version == '1.1':
            self.__broker = stomp.Connection11( broker_hosts )

        elif version == '1.2':
            self.__broker = stomp.Connection12( broker_hosts )

        else:
            raise Exception( "Invalid STOMPMQ_VERSION only '1.0', '1.1' or '1.2' are allowed" )

        # self.__listener = FlaskStompListener( self.__broker, app )
        self.__broker.set_listener( 'flask_app', self.__listener )
        self._connect()
        return

    @property
    def active( self ):
        return self.__app.config.get( "STOMPMQ_ENABLED", False )

    @property
    def username( self ):
        # type: () -> str
        return self.__username

    @property
    def password( self ):
        # type: () -> str
        return self.__password

    def _connect( self ):
        # type: () -> None
        if self.__connected:
            return
        
        logger.debug( 'Connect to Broker' )
        self.__broker.start()
        self.__broker.connect( self.__username, self.__password, wait = True )
        self.__connected  = True
        return

    def _disconnect( self ):
        # type: () -> None
        self.__broker.disconnect()
        self.__broker.stop()
        self.__connected  = False
        logger.debug( 'Disconnected from Broker' )
        return

    def _reconnect( self ):
        # type: () -> None
        self._disconnect()
        self._connect()
        return

    def subscribe( self, destination, id=1, ack='auto',
                   headers=None, **keyword_headers ):
        # type: (str, int) -> Tuple[int, int]
        """
        Subscribe to a certain queue.

        :param destination: a string specifying the subscription queue to
                            subscribe to.
        :param queue_id: 
        :param ack:
        :param headers:
        :param keyword_headers:

        :rtype: (int, int)
        :result: (result, mid)

        A queue is a UTF-8 string, which is used by the broker to filter
        messages for each connected client. A queue consists of one or more
        queue levels. Each queue level is separated by a forward slash
        (queue level separator).
        """
        if not self.__connected:
            self._reconnect()
            
        # try to subscribe
        self.__broker.subscribe( destination, id, ack, headers, **keyword_headers )
        self.__onSubscribe( destination = destination, 
                            id = id, 
                            ack = ack, 
                            header = headers, 
                            keyword_headers = keyword_headers )
        return

    def unsubscribe( self, destination ):
        # type: (str) -> void
        """
        Unsubscribe from a single queue

        :param destination: a single string that is the subscription queue to
                            unsubscribe from

        :rtype:             void
        :result:            None

        """
        # don't unsubscribe if not in queues
        for queue in self.__onSubscribe.getSubscriptions():
            if queue[ 'destination' ] == destination:
                self.__broker.unsubscribe( queue[ "id" ] )
                self.__onUnsubscribe( queue )

        return

    def unsubscribeAll( self ):
        # type: () -> None
        """Unsubscribe from all queues."""
        for queue in self.__onSubscribe.getSubscriptions():
            self.__broker.unsubscribe( queue[ 'id' ] )
            self.__onUnsubscribe( queue[ 'destination' ] )

        return

    def publish( self, destination, payload, content_type=None,
                 headers=None, **keyword_headers ):
        # type: ( str, bytes )
        """
        Send a message to the broker.

        :param destination: the topic that the message should be published on
        :param payload: the actual message to send. If not given, or set to
                        None a zero length message will be used. Passing an
                        int or float will result in the payload being
                        converted to a string representing that number.
                        If you wish to send a true int/float, use struct.pack()
                        to create the payload you require.

        :param content_type:
        :param headers:
        :param keyword_headers:

        :returns: Returns a tuple (result, mid), where result is
                  MQTT_ERR_SUCCESS to indicate success or MQTT_ERR_NO_CONN
                  if the client is not currently connected. mid is the message
                  ID for the publish request.

        """
        if not self.__connected:
            self._reconnect()

        self.__broker.send( destination, payload, content_type,
                          headers, keyword_headers )

        return

    def ack( self, message_id, queue_id ):
        """

        :param message_id:
        :param queue_id:
        :return:
        """
        return self.__broker.nack( message_id, queue_id )

    def nack( self, message_id, queue_id ):
        """

        :param message_id:
        :param queue_id:
        :return:
        """
        return self.__broker.nack( message_id, queue_id )

    def beginTransaction( self ):
        """Begin a transaction using the beginTransaction method, which returns
        the transaction id you then use when sending messages (you can also
        generate your own transaction id and pass that as a parameter to begin)

        :rtype:     str
        :return:    transactionId
        """
        return self.__broker.begin()

    def commitTransaction( self, transactionId ):
        """Commit a transaction and forward the messages

        :param transactionId:
        :return:
        """
        return self.__broker.commit( transactionId )

    def abortTransaction( self, transactionId ):
        """Abort a transaction and discard the sent messages

        :param transactionId:
        :return:
        """
        return self.__broker.abort( transactionId )


    '''
        Decorators
    '''
    def onError( self ):
        # type: () -> Callable
        """Decorator.

        Decorator to handle the event when connecting to the broker.
        Only the last decorated function will be called.
        """
        def decorator( handler ):
            # type: (Callable) -> Callable
            logger.debug( "Set onError handler on listener" )
            self.__listener._onError.set( handler )
            return handler

        return decorator
    
    def onConnecting( self ):
        # type: () -> Callable
        """Decorator.

        Decorator to handle the event when connecting to the broker.
        Only the last decorated function will be called.
        """
        def decorator( handler ):
            # type: (Callable) -> Callable
            logger.debug( "Set onConnecting handler on listener" )
            self.__listener._onConnecting.set( handler )
            return handler

        return decorator


    def onConnected( self ):
        # type: () -> Callable
        """Decorator.

        Decorator to handle the event when the broker responds to a connection
        request. Only the last decorated function will be called.

        """
        def decorator( handler ):
            # type: (Callable) -> Callable
            logger.debug( "Set onConnected handler on listener" )
            self.__listener._onConnected.set( handler )
            return handler

        return decorator

    def onDisconnect( self ):
        # type: () -> Callable
        """Decorator.

        Decorator to handle the event when client disconnects from broker. Only
        the last decorated function will be called.

        """
        def decorator( handler ):
            # type: (Callable) -> Callable
            logger.debug( "Set onDiconnected handler on listener" )
            self.__listener._onDisconnected.set( handler )
            return handler

        return decorator

    def onHeartbeat( self ):
        """Decorator.

        Decorator to handle the event when a heartbeat is received from broker. Only
        the last decorated function will be called.

        """
        def decorator( handler ):
            # type: (Callable) -> Callable
            logger.debug( "Set onHeartbeat handler on listener" )
            self.__listener._onHeartbeat.set( handler )
            return handler

        return decorator

    def onHeartbeatTimeout( self ):
        # type: () -> Callable
        """Decorator.

        Decorator to handle the event when a heartbeat timesout from broker. Only
        the last decorated function will be called.

        """
        def decorator( handler ):
            # type: (Callable) -> Callable
            logger.debug( "Set onHeartbeatTimeout handler on listener" )
            self.__listener._onHeartbeatTimeout.set( handler )
            return handler

        return decorator

    def onReceiverLoopCompleted( self ):
        """Called when the connection receiver_loop has finished.

        :return:
        """
        def decorator( handler ):
            logger.debug( "Set onReceiverLoopCompleted handler on listener" )
            self.__listener._onReceiverLoopCompleted.set( handler )
            return handler

        return decorator

    def onBeforeMessage( self, **kwargs ):
        # type: () -> Callable
        """Decorator.

        :param queue:
        Decorator to handle

        """
        def decorator( handler ):
            # type: (Callable) -> Callable
            logger.debug( "Set onBeforeMessage handler on listener" )
            self.__listener._onBeforeMessage.append( handler, **kwargs )

            return handler

        return decorator

    def onMessage( self, **kwargs ):
        # type: () -> Callable
        """Decorator.

        Decorator to handle all messages that have been subscribed and that
        are not handled via the `on_message` decorator.

        :param queue:
        
        **Example Usage:**::

            @stompConnector.on_message()
            def handle_messages( headers, body ):
                print('Received message on topic {}: {}'.format( headers, body ) )

        """
        def decorator( handler ):
            # type: (Callable) -> Callable
            logger.debug( "Set onMessage handler on listener" )
            self.__listener._onMessage.append( handler, **kwargs )
            return handler

        return decorator

    def onReceipt( self, **kwargs ):
        # type: () -> Callable
        """Decorator.

        Decorator to handle all messages that have been subscribed and that
        are not handled via the `on_message` decorator.
        
        :param queue:
        
        
        **Example Usage:**::

            @stompConnector.on_message()
            def handle_messages( headers, body ):
                print('Received message on topic {}: {}'.format( headers, body ) )

        """
        def decorator( handler ):
            # type: (Callable) -> Callable
            logger.debug( "Set onMessage handler on listener" )
            self.__listener._onReceipt.append( handler, **kwargs )
            return handler

        return decorator

    def onSend( self, **kwargs ):
        # type: () -> Callable
        """Decorator.

        Decorator to handle all messages that have been published by the
        client.
        
        :param queue:

        **Example Usage:**::

            @stompConnector.on_publish()
            def handle_send( frame ):
                print( 'Published message with frame {}.'.format( frame ) )
        """
        def decorator( handler ):
            # type: (Callable) -> Callable
            logger.debug( "Set onSend handler on listener" )
            self.__listener._onSend( handler, **kwargs )
            return handler

        return decorator

    def onPublish( self, **kwargs ):
        # type: () -> Callable
        """Decorator.

        Decorator to handle all messages that have been published by the
        client.

        **Example Usage:**::

            @stompConnector.on_publish()
            def handle_publish( headers, body ):
                print('Published message with mid {}.'
                      .format(mid))
        """
        def decorator( handler ):
            # type: (Callable) -> Callable
            logger.debug( "Set onPublish handler on listener" )
            self.__listener._onSend.append( handler, **kwargs )
            return handler

        return decorator

    def onSubscribe( self, **kwargs ):
        # type: () -> Callable
        """Decorate a callback function to handle subscritions.

        **Usage:**::

            @stompConnector.onSubscribe()
            def handleSubscribe( client, userdata, mid, granted_qos ):
                print('Subscription id {} granted with qos {}.'
                      .format(mid, granted_qos))
        """
        def decorator( handler ):
            # type: (Callable) -> Callable
            logger.debug( "Set onSubscribe handler on listener" )
            self.__onSubscribe.append( handler, **kwargs )
            return handler

        return decorator

    def onUnsubscribe( self, **kwargs ):
        # type: () -> Callable
        """Decorate a callback funtion to handle unsubscribtions.

        **Usage:**::

            @stompConnector.unsubscribe()
            def handle_unsubscribe(client, userdata, mid)
                print('Unsubscribed from topic (id: {})'
                      .format(mid)')
        """
        def decorator( handler ):
            # type: (Callable) -> Callable
            logger.debug( "Set onUnsubscribe handler on listener" )
            self.__onUnsubscribe.append( handler, **kwargs )
            return handler

        return decorator

