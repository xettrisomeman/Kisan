# codespaces-quickstart
Get started with Rasa Pro in the browser using GitHub Codespaces.

### Steps

1. **Create a Codespace:**
   - Click on the green "Code" button on this page, then scroll down to "Codespaces".
   - Click on "Create codespace on main".

2. **Set Up Environment:**
   - In the codespace, open the `.env` file from this repo and add your license key to that file.
     ```
     RASA_PRO_LICENSE='your_rasa_pro_license_key_here'
     COHERE_API_KEY='your_cohere_api_key_here'
     ```
   - Set this environment variables by running 
     ```
     source .env
     ```
   - Activate your python environment by running
     ```
     source .venv/bin/activate
     ```
   - Install Requied libraries
      ```
      uv pip install -r req.txt
      ```

3. **Train the Model:**
   - In the terminal, run:
     ```
     rasa train
     ```

4. **Run Fastapi Server:**
    - In the terminal, run:
      ```
      cd rest_client/
      fastapi run main.py --reload
      ```

4. **Talk to your Bot:**
   - In the terminal, run
     ```
     rasa inspect
     ```
     GitHub will show a notification, click on the green button to view the inspector where you can chat with your assistant.

5. **Run Custom Actions:**
  In Rasa 3.10 and later, custom actions are automatically run as part of your running assistant. To double-check that this is set up correctly, ensure that your `endpoints.yml` file contains the following configuration:
   ```
   action_endpoint:
      actions_module: "actions" # path to your actions package
    ```
   Then re-run your assistant via `rasa inspect` every time you make changes to your custom actions.


### Commands
  - list goods
  - register 
  - login
  - add goods
    - edit
    - delete
    - buy
  - check purchase order pending
    - cancel
  - check incoming order
    - accept
  - check recent activities
  - ask expert / message to experts
  - check messages history
  - logout