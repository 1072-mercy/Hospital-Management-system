function addService() {
  var servicesContainer = document.getElementById("servicesContainer");
  var serviceCount = servicesContainer.children.length;
  
  var newServiceItem = document.createElement("div");
  newServiceItem.classList.add("serviceItem");
  
  newServiceItem.innerHTML = `
    <label for="service${serviceCount}">Service:</label>
    <select class="service" id="service${serviceCount}">
      <option value="consultation">Consultation (KSH2000)</option>
      <option value="DIALYSIS">DIALYSIS (KSH1000)</option>
      <option value="bloodTest">Blood Test (KSH500)</option>
    </select>

    <label for="quantity${serviceCount}">Quantity:</label>
    <input type="number" class="quantity" id="quantity${serviceCount}" min="1" value="1" required><br><br>
  `;
  
  servicesContainer.appendChild(newServiceItem);
}

// Function to calculate the total bill amount
function calculateTotal() {
  var total = 0;
  var services = document.getElementsByClassName("service");
  var quantities = document.getElementsByClassName("quantity");
  
  for (var i = 0; i < services.length; i++) {
    var service = services[i].value;
    var quantity = parseInt(quantities[i].value);
    
    switch (service) {
      case "consultation":
        total += 2000 * quantity;
        break;
      case "DIALYSIS":
        total += 1000 * quantity;
        break;
      case "bloodTest":
        total += 500 * quantity;
        break;
    }
  }
  
  return total.toFixed(2);
}

// Function to update bill summary
function updateBillSummary() {
  var totalAmount = calculateTotal();
  document.getElementById("totalAmount").innerText = "Total Amount: KSH" + totalAmount;
}

// Event listener for form submission
document.getElementById("billingForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent the form from submitting
  
  var patientName = document.getElementById("patientName").value;
  var totalAmount = calculateTotal();

  alert("Patient Name: " + patientName + "\nTotal Amount: KSH" + totalAmount);
});

// Event listener for changes in services or quantities
document.getElementById("billingForm").addEventListener("change", updateBillSummary);