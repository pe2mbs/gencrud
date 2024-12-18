import os.path


angularPath = r'\src\python\testrun-web\frontend-v12\src\app'

modulePath  = r'\src\python\testrun-web\frontend-v12\src\app\wa-admin\access\screen.component.ts'

path = os.path.split( modulePath )[0]
length = len( path )
print( angularPath )
print( path )

while os.path.abspath( path ) != os.path.abspath( angularPath ):
    path = os.path.join( path, '..' )

print( path[ length + 1: ] )


