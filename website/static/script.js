document.querySelectorAll("#delete").forEach(button => {
    button.addEventListener("click", () => {
        Swal.fire({
            title: "¿Estás seguro/a de eliminar este poema?",
            text: "Esta acción no se puede revertir.",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Eliminar",
            cancelButtonText: "Cancelar"
        }).then(r => {
            if (r.isConfirmed) window.location.href = `/poema/${button.getAttribute("data-poem-id")}/delete`;
        });
    });
});