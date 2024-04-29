#!/bin/bash

# Jalankan behave
behave
allure serve allure_behave.formatter:AllureFormatter.output
echo "Allure report generated successfully."

