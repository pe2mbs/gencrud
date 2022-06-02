import webapp2.api as API
import posixpath
import pytz
import flask_monitoringdashboard as dashboard
import flask_monitoringdashboard.core.config


class DashboardConfig( flask_monitoringdashboard.core.config.Config ):
    """This class overrides the standard configuration class of the Flask monitoring dashboard
    to support loading the configuration from the main application configuration

    """
    def __init__(self):
        flask_monitoringdashboard.core.config.Config.__init__( self )
        return

    def init_from_config( self, configuration, key = 'FLASK_MONITORING_DASHBOARD' ):
        # Check parameter and presence og the key in the configuration
        if not isinstance( configuration, dict ) and key in configuration:
            return False

        # Extract the Flask monitoring dashboard configuration
        dictionary              = configuration.get( key, {} )
        # Set the parameters (override)
        self.version            = str( dictionary.get( 'VERSION', self.version ) )
        self.blueprint_name     = dictionary.get( 'LINK', self.blueprint_name )
        self.link               = dictionary.get( 'LINK', self.link )
        API.logger.info( "Flask monitoring dashboard available at {}".format(
            posixpath.join( configuration.get( 'HOSTNAME', 'http://localhost' ),
                            self.link ) ) )
        self.monitor_level      = dictionary.get( 'MONITOR_LEVEL', self.monitor_level )
        self.outlier_detection_constant = dictionary.get( 'OUTLIER_DETECTION_CONSTANT', self.outlier_detection_constant )
        self.sampling_period    = dictionary.get( 'SAMPLING_PERIOD', self.sampling_period )
        self.enable_logging     = dictionary.get( 'ENABLE_LOGGING', self.enable_logging )
        # database
        self.database_name      = dictionary.get( 'DATABASE', self.database_name )
        self.table_prefix       = dictionary.get( 'TABLE_PREFIX', self.table_prefix )
        # authentication
        self.username           = dictionary.get( 'USERNAME', self.username )
        self.password           = dictionary.get( 'PASSWORD', self.password )
        self.security_token     = dictionary.get( 'SECURITY_TOKEN', self.security_token )
        try:
            self.timezone           = pytz.timezone( dictionary.get( 'TIMEZONE', self.timezone.zone ) )

        except pytz.UnknownTimeZoneError:
            API.logger.error( 'Flask monitoring dashboard, using default timezone, which is UTC' )
            self.timezone = pytz.timezone('UTC')

        # visualization
        self.colors             = dictionary.get( 'COLORS', self.colors )
        return True


# Setup the custom config class
dashboard.config = DashboardConfig()
