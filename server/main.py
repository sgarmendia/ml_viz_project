from app import app
from config import PORT, DEV

import routes.root_routes

if __name__ == "__main__":
    app.run(debug=DEV, port=PORT, host='0.0.0.0')