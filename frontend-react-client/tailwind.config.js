/** @type {import('tailwindcss').Config} */

import { darken, lighten } from 'polished';

module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],  
  theme: {
    extend: {
      colors: {
        // Main call-to-action color (determines the overall look and feel)
        primary: {  
          DEFAULT: '#DD6031',         
          dark: darken(0.1, '#DD6031'), 
          light: lighten(0.1, '#DD6031'),
        },
        // Optional secondary call-to-action color (accent color)
        secondary: {  
          DEFAULT: '#124E78',         
          dark: darken(0.1, '#124E78'), 
          light: lighten(0.1, '#124E78'),
        },
        
        // Optional tertiary call-to-action color
        tertiary: {  
          DEFAULT: '#57737A',         
          dark: darken(0.1, '#57737A'), 
          light: lighten(0.1, '#57737A'),
        }, 
        // Background color
        bgColor: {  
          DEFAULT: '#EAEAEA',   // platinum   
          dark: darken(0.1, '#EAEAEA'), 
          light: lighten(0.1, '#EAEAEA'),
        },
        // Text color
        textColor: {  
          DEFAULT: '#000000',         
          dark: darken(0.1, '#000000'), 
          light: lighten(0.1, '#000000'),
        },
        // Border color
        borderColor: {  
          DEFAULT: '#56666B',         
          dark: darken(0.1, '#56666B'), 
          light: lighten(0.1, '#56666B'),
        },
        // Feedback colors
        successColor: '#8EA604',   // green
        errorColor: '#BF211E',     // red
        warningColor: '#F5BB00',   // yellow
      },
    },
  },
  plugins: [],
}

