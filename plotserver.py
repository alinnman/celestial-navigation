'''
    NMEA 0183 TCP Server for Marine GPS/Plotter Integration.
    Refactored with proper resource management and thread safety.

    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)  
'''

import socket
import threading
import time
from datetime import datetime, timezone
from typing import Optional, List, Tuple

# pylint: disable=R0902
class NMEAServer:
    """Thread-safe NMEA 0183 server implementation"""

    def __init__(self, host='0.0.0.0', port=10110):
        self.host = host
        self.port = port
        self.clients: List[socket.socket] = []
        self.clients_lock = threading.Lock()
        self.running = False
        self.server_socket: Optional[socket.socket] = None

        # Position data with thread safety
        self.position_lock = threading.Lock()
        self.latitude = 0.0
        self.longitude = 0.0
        self.last_update: Optional[datetime] = None

        # Track threads for proper cleanup
        self.broadcast_thread: Optional[threading.Thread] = None
        self.accept_thread: Optional[threading.Thread] = None
        self.client_threads: List[threading.Thread] = []

    def calculate_checksum(self, sentence: str) -> str:
        """Calculate NMEA checksum (XOR of all characters)"""
        checksum = 0
        for char in sentence:
            checksum ^= ord(char)
        return f"{checksum:02X}"

    def format_coordinate(self, coord: float, is_longitude: bool = False) -> str:
        """Convert decimal degrees to NMEA format"""
        abs_coord = abs(coord)
        degrees = int(abs_coord)
        minutes = (abs_coord - degrees) * 60

        if is_longitude:
            return f"{degrees:03d}{minutes:06.3f}"
        else:
            return f"{degrees:02d}{minutes:06.3f}"

    def create_gga_sentence(self) -> str:
        """Create NMEA GGA sentence (Global Positioning System Fix Data)"""
        now = datetime.now(timezone.utc)
        time_str = now.strftime("%H%M%S.%f")[:-3]

        with self.position_lock:
            lat = self.latitude
            lon = self.longitude

        lat_str = self.format_coordinate(abs(lat))
        lat_dir = 'N' if lat >= 0 else 'S'
        lon_str = self.format_coordinate(abs(lon), True)
        lon_dir = 'E' if lon >= 0 else 'W'

        sentence = \
        f"GPGGA,{time_str},{lat_str},{lat_dir},{lon_str},{lon_dir},1,08,1.0,10.0,M,0.0,M,,"
        checksum = self.calculate_checksum(sentence)
        return f"${sentence}*{checksum}\r\n"

    def create_rmc_sentence(self) -> str:
        """Create NMEA RMC sentence"""
        now = datetime.now(timezone.utc)
        time_str = now.strftime("%H%M%S.%f")[:-3]
        date_str = now.strftime("%d%m%y")

        with self.position_lock:
            lat = self.latitude
            lon = self.longitude

        lat_str = self.format_coordinate(abs(lat))
        lat_dir = 'N' if lat >= 0 else 'S'
        lon_str = self.format_coordinate(abs(lon), True)
        lon_dir = 'E' if lon >= 0 else 'W'

        sentence =\
        f"GPRMC,{time_str},A,{lat_str},{lat_dir},{lon_str},{lon_dir},0.0,0.0,{date_str},0.0,E"
        checksum = self.calculate_checksum(sentence)
        return f"${sentence}*{checksum}\r\n"

    def update_position(self, latitude: float, longitude: float):
        """Thread-safe position update"""
        with self.position_lock:
            self.latitude = latitude
            self.longitude = longitude
            self.last_update = datetime.now()
        # print(f"Position updated: {latitude:.6f}, {longitude:.6f}") REMOVED

    def handle_client(self, client_socket: socket.socket, address: Tuple[str, int]):
        """Handle individual client connection"""
        print(f"Client connected from {address}")

        with self.clients_lock:
            self.clients.append(client_socket)

        try:
            # Keep connection alive while server is running
            while self.running:
                time.sleep(1)
# pylint: disable=W0718
        except Exception as e:
# pylint: enable=W0718
            print(f"Client {address} error: {e}")
        finally:
            with self.clients_lock:
                if client_socket in self.clients:
                    self.clients.remove(client_socket)
            try:
                client_socket.close()
# pylint: disable=W0702
            except:
                pass
# pylint: enable=W0702
            print(f"Client {address} disconnected")

    def broadcast_data(self):
        """Broadcast NMEA data to all connected clients"""
        print("Broadcast thread started")

        while self.running:
            with self.position_lock:
                has_position = self.last_update is not None

            if has_position:
                with self.clients_lock:
                    clients_copy = self.clients.copy()

                if clients_copy:
                    gga_sentence = self.create_gga_sentence()
                    rmc_sentence = self.create_rmc_sentence()
                    data = (gga_sentence + rmc_sentence).encode('ascii')

                    disconnected = []
                    for client in clients_copy:
                        try:
                            client.send(data)
# pylint: disable=W0718
                        except Exception as e:
# pylint: enable=W0718
                            print(f"Error sending to client: {e}")
                            disconnected.append(client)

                    # Clean up disconnected clients
                    if disconnected:
                        with self.clients_lock:
                            for client in disconnected:
                                if client in self.clients:
                                    self.clients.remove(client)
                                try:
                                    client.close()
# pylint: disable=W0702
                                except:
                                    pass
# pylint: disable=W0702

            time.sleep(1)  # Send data every second

        print("Broadcast thread stopped")

    def _accept_connections(self):
        """Accept incoming client connections (runs in separate thread)"""
        print("Accept thread started")

        while self.running:
            try:
                # Set timeout so we can check self.running periodically
                if self.server_socket:
                    self.server_socket.settimeout(1.0)
                    try:
                        try:
                            client_socket, address = self.server_socket.accept()
                        except socket.timeout:
                            continue

                        # Create and track client thread
                        client_thread = threading.Thread(
                            target=self.handle_client,
                            args=(client_socket, address),
                            name=f"Client-{address}",
                            daemon=True
                        )
                        self.client_threads.append(client_thread)
                        client_thread.start()

                    except socket.timeout:
                        continue  # Check self.running again
# pylint: disable=W0718
            except Exception as e:
# pylint: enable=W0718
                if self.running:
                    print(f"Error accepting connection: {e}")
                break

        print("Accept thread stopped")

    def start(self):
        """Start the NMEA server"""
        if self.running:
            print("Server already running")
            return

        self.running = True
        print(f"Starting NMEA server on {self.host}:{self.port}")

        try:
            # Create and configure server socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"NMEA server listening on {self.host}:{self.port}")

            # Start broadcast thread
            self.broadcast_thread = threading.Thread(
                target=self.broadcast_data,
                name="NMEA-Broadcast",
                daemon=True
            )
            self.broadcast_thread.start()

            # Start accept thread
            self.accept_thread = threading.Thread(
                target=self._accept_connections,
                name="NMEA-Accept",
                daemon=True
            )
            self.accept_thread.start()

            print("NMEA server started successfully")

        except Exception as e:
            print(f"Server startup error: {e}")
            self.stop()
            raise

    def stop(self):
        """Stop the NMEA server and clean up all resources"""
        if not self.running:
            return

        print("Stopping NMEA server...")
        self.running = False

        # Close server socket (this will break accept loop)
        if self.server_socket:
            try:
                self.server_socket.close()
# pylint: disable=W0718
            except Exception as e:
# pylint: enable=W0718
                print(f"Error closing server socket: {e}")
            self.server_socket = None

        # Wait for accept thread
        if self.accept_thread and self.accept_thread.is_alive():
            self.accept_thread.join(timeout=3.0)
            if self.accept_thread.is_alive():
                print("Warning: Accept thread didn't stop cleanly")

        # Wait for broadcast thread
        if self.broadcast_thread and self.broadcast_thread.is_alive():
            self.broadcast_thread.join(timeout=3.0)
            if self.broadcast_thread.is_alive():
                print("Warning: Broadcast thread didn't stop cleanly")

        # Close all client connections
        with self.clients_lock:
            for client in self.clients:
                try:
                    client.close()
# pylint: disable=W0702
                except:
                    pass
# pylint: enable=W0702
            self.clients.clear()

        # Wait for client threads (with timeout to avoid infinite wait)
        for thread in self.client_threads:
            if thread.is_alive():
                thread.join(timeout=1.0)
        self.client_threads.clear()

        print("NMEA server stopped")


class PlotServerManager:
    """
    Singleton manager for NMEA plot server lifecycle.
    Ensures only one server instance runs and provides proper cleanup.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    instance = super().__new__(cls)
                    # Initialize the flag here so __init__ can check it
                    instance._initialized = False
                    cls._instance = instance
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.server: Optional[NMEAServer] = None
        self.server_thread: Optional[threading.Thread] = None
        self.is_running = False
        self.kill_timer: Optional[threading.Timer] = None
        self._initialized = True
        print("PlotServerManager initialized")

    def start(self):
        """Start the plot server (idempotent - safe to call multiple times)"""
        with self._lock:
            if self.is_running:
                print("PlotServerManager: Server already running, resetting kill timer")
                self._reset_kill_timer()
                return

            print("PlotServerManager: Starting new server")

            # Create new server instance
            self.server = NMEAServer(host='0.0.0.0', port=10110)
            self.is_running = True  # ← Change this line

            # Start server in dedicated thread
            self.server_thread = threading.Thread(
                target=self.server.start,
                name="PlotServerMain",
                daemon=True
            )
            self.server_thread.start()

            # Start automatic shutdown timer
            self._reset_kill_timer()

            print("PlotServerManager: Server started")

    def _reset_kill_timer(self):
        """Reset the automatic shutdown timer (20 seconds of inactivity)"""
        # Cancel existing timer
        if self.kill_timer:
            self.kill_timer.cancel()

        # Create new timer
        self.kill_timer = threading.Timer(20.0, self._auto_shutdown)
        self.kill_timer.daemon = True
        self.kill_timer.start()

    def _auto_shutdown(self):
        """Automatically shutdown server after inactivity"""
        print("PlotServerManager: Auto-shutdown triggered (20s inactivity)")
        self.stop()

    def update_position(self, lat: float, lon: float):
        """Update position and reset kill timer"""
        with self._lock:
            if self.server and self.is_running:
                self.server.update_position(lat, lon)
                self._reset_kill_timer()
            else:
                print("PlotServerManager: Server not running, cannot update position")

    def stop(self):
        """Stop the plot server and clean up resources"""
        with self._lock:
            if not self.is_running:
                print("PlotServerManager: Server not running, nothing to stop")
                return

            print("PlotServerManager: Stopping server")

            # Cancel kill timer
            if self.kill_timer:
                self.kill_timer.cancel()
                self.kill_timer = None

            # Stop server
            if self.server:
                self.server.stop()
                self.server = None

            # Wait for server thread
            if self.server_thread and self.server_thread.is_alive():
                self.server_thread.join(timeout=5.0)
                if self.server_thread.is_alive():
                    print("PlotServerManager: Warning - server thread didn't stop cleanly")

            self.is_running = False
            self.server_thread = None

            print("PlotServerManager: Server stopped and cleaned up")

    def get_status(self) -> dict:
        """Get current server status (for debugging)"""
        with self._lock:

            status: dict[str, int | bool] = {
                'is_running': self.is_running,
                'server_thread_alive':\
                    self.server_thread.is_alive() if self.server_thread else False,
                'has_server': self.server is not None,
            }

            if self.server:
                with self.server.clients_lock:
                    status['client_count'] = len(self.server.clients)
                with self.server.position_lock:
                    status['has_position'] = self.server.last_update is not None

            return status
# pylint: enable=R0902


# Create singleton instance
plot_server = PlotServerManager()


# Convenience functions for backward compatibility
def start_plotserver():
    """Start the plot server"""
    plot_server.start()


def kill_plotserver():
    """Stop the plot server"""
    plot_server.stop()


def update_plot_position(lat: float, lon: float):
    """Update the plot server with new coordinates"""
    plot_server.update_position(lat, lon)


def main():
    """Example usage"""
    print("Starting NMEA server test...")

    try:
        plot_server.start()

        # Simulate position updates
        while True:
            try:
                lat = float(input("Enter latitude (or 'q' to quit): "))
                lon = float(input("Enter longitude: "))
                plot_server.update_position(lat, lon)

                # Show status
                status = plot_server.get_status()
                print(f"Server status: {status}")

            except ValueError:
                print("Invalid coordinates")
            except (KeyboardInterrupt, EOFError):
                break

    finally:
        print("\nShutting down...")
        plot_server.stop()
        print("Done!")


if __name__ == "__main__":
    main()
