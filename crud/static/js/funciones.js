
const btndelete = document.querySelectorAll('.btn-delete')
//console.log(btndelete)
if (btndelete) {

    /** se crea una constante 
     * con el arreglo para 
     * recorrer todos los botones */
    const btnarray = Array.from(btndelete);
    btnarray.forEach((btn) => {
      
        /** se agrega un 
         * envento click por 
         * cada boton de borrar 
         * */
        btn.addEventListener('click', (e) => {

            /** y al hacerle click 
             * pregunta si estas seguro.... */
            if (!confirm("¿Estas seguro de querer eliminarlo?")) {
                e.preventDefault();
            }
        });
    });
}   




const select_tipo = document.querySelector('#tipo');
select_tipo.addEventListener("change", ()=> {
	// obtengo el objeto html
    tipo = document.getElementById('tipo');
    var datos = {
        // asigno a tipo el valor del objeto
        tipo : tipo.value
    };

    fetch('/genera_codigo', {
		method : 'POST',
		body : JSON.stringify(datos),
        cache:"no-cache",
        headers : {'Content-Type': 'application/json'}
	})
    .then(function (response) {
        if (response.status!==200) {
            console.log(`Response Status no es 200: "${response.status}`);
            return ;
        }
        response.json().then(function(data) {
            console.log(data);
            aux=data['data'];
            document.getElementById('codigo').value=aux
            
        })
    })
});
