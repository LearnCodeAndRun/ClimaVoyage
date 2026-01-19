const cityInput = document.getElementById("cityInput");
const cityList = document.getElementById("cityList");
const weatherResult = document.getElementById("weatherResult");

let timer = null;

cityInput.addEventListener("input", () => {
  clearTimeout(timer);

  const query = cityInput.value.trim();

  if (query.length < 2) {
    cityList.innerHTML = "";
    return;
  }

  timer = setTimeout(() => {
    fetch(`/search-city?q=${query}`)
      .then(res => res.json())
      .then(data => {
        cityList.innerHTML = "";

        data.forEach(city => {
          const li = document.createElement("li");
          li.className = "list-group-item list-group-item-action";
          li.textContent = `${city.name}, ${city.state} ${city.country}`;

          li.onclick = () => {
            cityInput.value = city.name;
            cityList.innerHTML = "";
            fetchWeather(city.lat, city.lon);
          };

          cityList.appendChild(li);
        });
      });
  }, 300);
});

function fetchWeather(lat, lon) {
  fetch(`/weather?lat=${lat}&lon=${lon}`)
    .then(res => res.json())
    .then(data => {
      weatherResult.innerHTML = `
        <h4>${data.city}</h4>
        <p>🌡 Temperature: ${data.temperature}°C</p>
        <p>🤔 Feels Like: ${data.feels_like}°C</p>
        <p>💧 Humidity: ${data.humidity}%</p>
        <p>🌥 Condition: ${data.description}</p>
      `;
    });
}
