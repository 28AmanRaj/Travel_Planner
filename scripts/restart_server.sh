#!/bin/bash
# Restart the application server (LessonPlan Generator)

# Restart the service
echo "Restarting the travel-planner service..."
sudo systemctl restart travel-planner

# Check the status of the service
echo "Fetching the status of the travel_planner service..."
sudo systemctl status travel-planner --no-pager