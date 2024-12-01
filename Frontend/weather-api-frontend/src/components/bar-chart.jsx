import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

// Register required components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const data = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr'], // Group labels
  datasets: [
    {
      label: 'Szél (mm)', 
      data: [12, 19, 3, 5],
      backgroundColor: 'rgba(75, 192, 192, 0.6)', //blueish
    },
    {
      label: 'Hőmérséklet (°C)', // Second bar in each group
      data: [22, 25, 27, 28],
      backgroundColor: 'rgba(255, 99, 132, 0.6)', //redish
    },
    {
      label: 'Csapadék (%)', // Third bar in each group
      data: [50, 45, 60, 55],
      backgroundColor: 'rgba(54, 162, 235, 0.6)', // greenish
    },
  ],
};

const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'Weather Data (Multiple Bars per Label)',
    },
  },
  scales: {
    x: {
      stacked: false, // Set to true for stacked bars
      title: {
        display: true,
        text: 'Months',
      },
    },
    y: {
      stacked: false, // Set to true for stacked bars
      title: {
        display: true,
        text: '',
      },
      beginAtZero: true,
    },
  },
};

const MultiBarChart = () => {
  return <Bar data={data} options={options} />;
};

export default MultiBarChart;
