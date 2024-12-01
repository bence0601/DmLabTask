
const fetchWeather = async (city) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/fetch-weather?city=${city}`);
      if (!response.ok) {
        throw new Error('Hiba történt a lekérdezés során');
      }
      const data = await response.json();
      console.log('Válasz a backendtől:', data);  // Kiírjuk a válasz tartalmát a konzolra
      return data;
    } catch (error) {
      console.error('Hiba történt az időjárás lekérdezése közben:', error);
      throw error;  
    }
  };
  
  export default fetchWeather;
  