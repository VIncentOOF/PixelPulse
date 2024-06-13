# Arduino Smart Planting Watering System

## How It Works

This Arduino-based system automatically waters your plants by monitoring the soil moisture level. Here's how it functions:

1. **Soil Moisture Detection**: The soil moisture sensor continuously reads the moisture level of the soil.
2. **Threshold Check**: If the moisture level is below a defined threshold, the relay is activated.
3. **Water Pump Activation**: When the relay is activated, it turns on the water pump to water the plant.
4. **Moisture Level Maintenance**: If the moisture level is above the threshold, the relay remains off, and the water pump does not operate.
5. **Continuous Monitoring**: The system continuously monitors the soil moisture level and controls the water pump accordingly to ensure optimal soil moisture for plant health.

## Notes

- **Adjust Threshold**: Adjust the threshold value based on your specific soil moisture sensor and plant requirements.
- **Proper Connections**: Ensure the relay module and water pump are properly powered and connected.
- **Safety Consideration**: For safety, consider adding a diode across the relay module's coil to protect against voltage spikes.

This system is ideal for automating plant watering, ensuring your plants receive the right amount of water based on the soil moisture level.

**IMPORTANT**:
This code is UNTESTED and subject to change, after receiving the board and pump