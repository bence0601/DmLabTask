import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels'; // Import the plugin

// Register the Chart.js components and the plugin
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ChartDataLabels);

const data = {
  labels: ['Jan', 'Feb', 'Mar'], // Group labels
  datasets: [
    {
      label: 'Szél (mph)', // First bar in each group
      data: [12, 19, 3], // Adjust data length to match labels
      backgroundColor: 'rgba(75, 192, 192, 0.6)', // greenish
      unit: 'mph', // Add unit for wind speed
    },
    {
      label: 'Hőmérséklet (°C)', // Second bar in each group
      data: [22, 25, 27], // Adjust data length to match labels
      backgroundColor: 'rgba(255, 99, 132, 0.6)', // redish
      unit: '°C', // Add unit for temperature
    },
    {
      label: 'Csapadék (mm)', // Third bar in each group
      data: [50, 45, 60], // Adjust data length to match labels
      backgroundColor: 'rgba(54, 162, 235, 0.6)', // blueish
      unit: 'mm', // Add unit for precipitation
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
      text: 'Időjárás adatok (Több oszlop címkék)',
    },
    // Enable datalabels plugin to display values on top of the bars
    datalabels: {
      color: 'black', // Label color
      font: {
        weight: 'bold', // Font weight for the values
        size: 14, // Font size for the values
      },
      align: 'end', // Align labels on top of the bars
      anchor: 'end', // Position the label at the end (top) of each bar
      formatter: (value, context) => {
        // Append the unit to each label
        const datasetIndex = context.datasetIndex;
        const unit = context.dataset.unit; // Access the unit defined in each dataset
        return `${value} ${unit}`; // Format the label to show value and unit
      },
    },
  },
  scales: {
    x: {
      stacked: false, // Set to true for stacked bars
      title: {
        display: true,
        text: 'Hónapok',
      },
    },
    y: {
      stacked: false, // Set to true for stacked bars
      title: {
        display: true,
        text: 'Értékek',
      },
      beginAtZero: true,
      display: false, // Hide the Y-axis values (numbers) on the side
    },
  },
};

const MultiBarChart = () => {
  return <Bar data={data} options={options} />;
};

export default MultiBarChart;
