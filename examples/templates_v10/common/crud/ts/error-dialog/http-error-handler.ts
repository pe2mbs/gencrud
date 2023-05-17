import Swal from "sweetalert2";


const htlmGenerator = ( errorResponse ) => {
    return "<p> Problem: " + ( errorResponse.error != null && errorResponse.error.problem != "" ? 
    errorResponse.error.problem : errorResponse.message  )+ "</p><br>" + 
    "<p> Solution: " +  (errorResponse.error.solution != "" ? 
    errorResponse.error.solution : "Contact developer team") + "</p>"
}

export const commonErrorHandler = (errorResponse, next?: () => void ) => {
    Swal.fire({
        position: 'center',
        icon: 'error',
        title: 'Something went wrong. Please try again or contact the developers.',
        html: htlmGenerator( errorResponse ),
        showConfirmButton: true
    });
    if ( next ) {
        next();
    }
}

export const redirectingErrorHandler = (errorResponse, path: string, next?: () => void ) => {
    Swal.fire({
        position: 'center',
        icon: 'error',
        title: 'Uups, an error appeared',
        html: htlmGenerator( errorResponse ),
        confirmButtonText: 'Back to Dashboard',
        showConfirmButton: true,
        backdrop: false, // dont close without button click
    }).then( result => {
        if (result.isConfirmed) {
            window.location.href = path; //relative to domain
        }
    })
    if ( next ) {
        next();
    }
}