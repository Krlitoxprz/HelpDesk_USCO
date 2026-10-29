// Contador de caracteres para ayudar al usuario a redactar la descripción.
document.addEventListener("DOMContentLoaded", () => {
  const DescriptionField = document.getElementById("description");
  const DescriptionCount = document.getElementById("description-count");
  // Estos elementos solo están presentes en el formulario de creación.
  if (DescriptionField && DescriptionCount) {
    const UpdateCount = () => { DescriptionCount.textContent = DescriptionField.value.length; };
    DescriptionField.addEventListener("input", UpdateCount);
    UpdateCount();
  }
});
