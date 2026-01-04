"""
Flask Application for Adaptive Traffic Control System
Main backend server handling image uploads and traffic control logic.
"""
import os
import json
from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
import traffic_density
import traffic_controller

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store current traffic state
current_state = {
    'densities': {},
    'green_times': {},
    'active_road': None,
    'remaining_time': 0,
    'cycle_active': False
}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_images():
    """
    Handle image uploads for all four directions.
    Expected: 4 images with keys: 'north', 'south', 'east', 'west'
    """
    if 'north' not in request.files or 'south' not in request.files or \
       'east' not in request.files or 'west' not in request.files:
        return jsonify({'error': 'Missing images. Please upload images for all 4 directions.'}), 400
    
    road_mapping = {
        'north': 'North',
        'south': 'South',
        'east': 'East',
        'west': 'West'
    }
    
    densities = {}
    uploaded_files = {}
    
    try:
        # Process each direction
        for key, road_name in road_mapping.items():
            file = request.files[key]
            
            if file.filename == '':
                return jsonify({'error': f'No file selected for {road_name}'}), 400
            
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{key}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                uploaded_files[key] = filepath
                
                # Estimate traffic density
                density = traffic_density.estimate_traffic_density(filepath)
                densities[road_name] = density
        
        # Calculate green times
        green_times = traffic_controller.calculate_green_times(
            densities,
            min_green_time=5,
            max_green_time=30,
            total_cycle_time=60
        )
        
        # Select active road (highest density)
        active_road = traffic_controller.select_active_road(densities)
        
        # Update current state
        current_state['densities'] = densities
        current_state['green_times'] = green_times
        current_state['active_road'] = active_road
        current_state['remaining_time'] = green_times.get(active_road, 5)
        current_state['cycle_active'] = True
        
        # Get signal states
        signal_states = traffic_controller.get_signal_states(
            active_road,
            list(road_mapping.values())
        )
        
        return jsonify({
            'success': True,
            'densities': densities,
            'green_times': green_times,
            'active_road': active_road,
            'signal_states': signal_states,
            'remaining_time': current_state['remaining_time']
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing images: {str(e)}'}), 500


@app.route('/api/state', methods=['GET'])
def get_state():
    """Get current traffic control state."""
    signal_states = {}
    if current_state['active_road']:
        signal_states = traffic_controller.get_signal_states(
            current_state['active_road'],
            ['North', 'South', 'East', 'West']
        )
    
    return jsonify({
        'densities': current_state['densities'],
        'green_times': current_state['green_times'],
        'active_road': current_state['active_road'],
        'remaining_time': current_state['remaining_time'],
        'signal_states': signal_states,
        'cycle_active': current_state['cycle_active']
    })


@app.route('/api/tick', methods=['POST'])
def tick():
    """
    Decrement the countdown timer.
    Called by frontend every second.
    """
    if current_state['cycle_active'] and current_state['remaining_time'] > 0:
        current_state['remaining_time'] -= 1
        
        # If time expired, switch to next road in cycle
        if current_state['remaining_time'] <= 0:
            # Cycle through roads based on green times
            roads = ['North', 'South', 'East', 'West']
            current_idx = roads.index(current_state['active_road']) if current_state['active_road'] in roads else 0
            next_idx = (current_idx + 1) % len(roads)
            next_road = roads[next_idx]
            
            current_state['active_road'] = next_road
            current_state['remaining_time'] = current_state['green_times'].get(next_road, 5)
    
    signal_states = {}
    if current_state['active_road']:
        signal_states = traffic_controller.get_signal_states(
            current_state['active_road'],
            ['North', 'South', 'East', 'West']
        )
    
    return jsonify({
        'remaining_time': current_state['remaining_time'],
        'active_road': current_state['active_road'],
        'signal_states': signal_states
    })


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset the traffic control system."""
    current_state['densities'] = {}
    current_state['green_times'] = {}
    current_state['active_road'] = None
    current_state['remaining_time'] = 0
    current_state['cycle_active'] = False
    
    return jsonify({'success': True, 'message': 'System reset'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
