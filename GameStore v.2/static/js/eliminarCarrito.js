function eliminarCarrito(numCarr){
    res=confirm("¿estas seguro de querer eliminar este juego del carrito? "+numCarr)
    if(res){
        location.assign("/eliminarCarrito/"+numCarr)
    }
}