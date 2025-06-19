import json
from concurrent.futures import ThreadPoolExecutor
import threading

@app.route('/run_unit_test', methods=['POST'])
def run_unit_test():
    try:
        # ...existing code...
        
        # Fix plot_details parsing
        plot_details_str = request.form.get('plot_details')
        if plot_details_str:
            try:
                # Parse JSON string to list of dictionaries
                plot_details_data = json.loads(plot_details_str)
                # Convert to proper schema format
                plot_details = [PlotDetails(**item) for item in plot_details_data]
            except (json.JSONDecodeError, TypeError) as e:
                return jsonify({
                    'success': False,
                    'message': f'Invalid plot_details format: {str(e)}'
                }), 400
        else:
            plot_details = []
            
        # ...existing code...
        
        # Run test with proper error handling for threading
        try:
            if hasattr(threading.current_thread(), '_is_main_thread'):
                result = method_to_test(*args, **kwargs)
            else:
                # Use ThreadPoolExecutor for non-main thread execution
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(method_to_test, *args, **kwargs)
                    result = future.result(timeout=30)
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Test execution failed: {str(e)}'
            }), 500
            
        # ...existing code...
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Request processing failed: {str(e)}'
        }), 400