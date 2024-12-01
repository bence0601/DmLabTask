const fetchWeather = async (city) => {
  try {
    console.log('City parameter:', city);  // Kiírja a város paramétert
    const response = await fetch(`http://127.0.0.1:5001/forecast-for-city?city=${city}`);
    
    if (!response.ok) {
      console.log(response);  // Ha a válasz nem OK, kiírja
      throw new Error('Hiba történt a lekérdezés során');
    }
    
    const data = await response.json();
    console.log('Válasz a backendtől:', data);  // Kiírja a válasz tartalmát
    return data;
  } catch (error) {
    console.error('Hiba történt az időjárás lekérdezése közben:', error);  // Hibakezelés
    throw error;  
  }
};

export default fetchWeather;
