const BASE_URL = "http://localhost:5000/api";

/** 
 * Generates HTML representation for a cupcake.
 * 
 * This function creates a block of HTML that contains the cupcake's flavor,
 * size, rating, and an image, along with a delete button.
 * 
 * @param {Object} cupcake - The cupcake data object containing properties: id, flavor, size, rating, and image.
 * @returns {string} - The HTML string representing the cupcake.
 */
function generateCupcakeHTML(cupcake) {
  return `
    <div data-cupcake-id=${cupcake.id}>
      <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="delete-button">X</button>
      </li>
      <img class="Cupcake-img"
           src="${cupcake.image}"
           alt="(no image provided)">
    </div>
  `;
}

/** 
 * Fetches the initial list of cupcakes from the server and displays them.
 * 
 * This function sends a GET request to the server to retrieve all cupcakes.
 * It then iterates over the received cupcake data, generates HTML for each cupcake,
 * and appends the HTML to the cupcakes list in the DOM.
 */
async function showInitialCupcakes() {
  const response = await axios.get(`${BASE_URL}/cupcakes`);
  const cupcakes = response.data.cupcakes;

  for (let cupcakeData of cupcakes) {
    let newCupcake = $(generateCupcakeHTML(cupcakeData));
    $("#cupcakes-list").append(newCupcake);
  }
}

/** 
 * Handles the submission of the new cupcake form.
 * 
 * This event handler captures the form data when the form is submitted.
 * It prevents the default form submission behavior, collects the input values,
 * sends a POST request to the server to create a new cupcake, and adds the
 * newly created cupcake to the list displayed on the page.
 */
$("#new-cupcake-form").on("submit", async function (evt) {
  evt.preventDefault();

  // Collect values from the form inputs
  let flavor = $("#form-flavor").val();
  let rating = $("#form-rating").val();
  let size = $("#form-size").val();
  let image = $("#form-image").val();

  // Send the form data to the server to create a new cupcake
  const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image
  });

  // Add the new cupcake to the list in the DOM
  let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
  $("#cupcakes-list").append(newCupcake);
  
  // Reset the form fields after submission
  $("#new-cupcake-form").trigger("reset");
});

/** 
 * Handles the deletion of a cupcake.
 * 
 * This event handler listens for clicks on delete buttons associated with cupcakes.
 * When a delete button is clicked, it sends a DELETE request to the server for the
 * corresponding cupcake. If successful, it removes the cupcake from the DOM.
 */
$("#cupcakes-list").on("click", ".delete-button", async function (evt) {
  evt.preventDefault();

  // Identify the cupcake element and retrieve its ID
  let $cupcake = $(evt.target).closest("div");
  let cupcakeId = $cupcake.attr("data-cupcake-id");

  // Send a request to delete the cupcake from the server
  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);

  // Remove the cupcake element from the DOM after deletion
  $cupcake.remove();
});

// Initialize the page with the existing cupcakes by calling showInitialCupcakes on page load
$(showInitialCupcakes);
