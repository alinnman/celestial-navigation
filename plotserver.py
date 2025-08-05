#!/usr/bin/env python3
"""
NMEA 0183 TCP Server for Marine GPS/Plotter Integration
Broadcasts position data in NMEA format over TCP connection
"""

import socket
import threading
import time
from datetime import datetime, timezone

class NMEAServer:
    ''' Implementation of NMEA 0183 server '''
    def __init__(self, host='0.0.0.0', port=10110):
        self.host = host
        self.port = port
        self.clients = []
        self.running = False
        self.server_socket = None

        # Current position data
        self.latitude = 0.0
        self.longitude = 0.0
        self.last_update = None

    def calculate_checksum(self, sentence):
        """Calculate NMEA checksum (XOR of all characters between $ and *)"""
        checksum = 0
        for char in sentence[1:]:  # Skip the $
            checksum ^= ord(char)
        return f"{checksum:02X}"

    def format_coordinate(self, coord, is_longitude=False):
        """Convert decimal degrees to NMEA format (DDMM.MMMM or DDDMM.MMMM)"""
        abs_coord = abs(coord)
        degrees = int(abs_coord)
        minutes = (abs_coord - degrees) * 60

        if is_longitude:
            return f"{degrees:03d}{minutes:06.3f}"
        else:
            return f"{degrees:02d}{minutes:06.3f}"

    def create_gga_sentence(self):
        """Create NMEA GGA sentence (Global Positioning System Fix Data)"""
        now = datetime.now(timezone.utc)
        time_str = now.strftime("%H%M%S.%f")[:-3]  # HHMMSS.SSS

        lat_str = self.format_coordinate(abs(self.latitude))
        lat_dir = 'N' if self.latitude >= 0 else 'S'

        lon_str = self.format_coordinate(abs(self.longitude), True)
        lon_dir = 'E' if self.longitude >= 0 else 'W'

        # Build sentence without checksum
        sentence =\
        f"GPGGA,{time_str},{lat_str},{lat_dir},{lon_str},{lon_dir},1,08,1.0,10.0,M,0.0,M,,"

        # Add checksum
        checksum = self.calculate_checksum(sentence)
        return f"${sentence}*{checksum}\r\n"

    def create_rmc_sentence(self):
        """Create NMEA RMC sentence (Recommended Minimum Navigation Information)"""
        now = datetime.now(timezone.utc)
        time_str = now.strftime("%H%M%S.%f")[:-3]  # HHMMSS.SSS
        date_str = now.strftime("%d%m%y")  # DDMMYY

        lat_str = self.format_coordinate(abs(self.latitude))
        lat_dir = 'N' if self.latitude >= 0 else 'S'

        lon_str = self.format_coordinate(abs(self.longitude), True)
        lon_dir = 'E' if self.longitude >= 0 else 'W'

        # Build sentence without checksum (A=valid, V=invalid)
        sentence =\
        f"GPRMC,{time_str},A,{lat_str},{lat_dir},{lon_str},{lon_dir},0.0,0.0,{date_str},0.0,E"

        # Add checksum
        checksum = self.calculate_checksum(sentence)
        return f"${sentence}*{checksum}\r\n"

    def update_position(self, latitude, longitude):
        """Update the current position"""
        self.latitude = latitude
        self.longitude = longitude
        self.last_update = datetime.now()
        print(f"Position updated: {latitude:.6f}, {longitude:.6f}")

    def handle_client(self, client_socket, address):
        """Handle individual client connection"""
        print(f"Client connected from {address}")
        self.clients.append(client_socket)

        try:
            while self.running:
                # Client is handled by broadcast_data method
                time.sleep(1)
#pylint: disable=W0718
        except Exception as e:
            print(f"Client {address} error: {e}")
#pylint: enable=W0718
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
            print(f"Client {address} disconnected")

    def broadcast_data(self):
        """Broadcast NMEA data to all connected clients"""
        while self.running:
            if self.clients and self.last_update:
                # Create NMEA sentences
                gga_sentence = self.create_gga_sentence()
                rmc_sentence = self.create_rmc_sentence()

                # Send to all clients
                disconnected_clients = []
                for client in self.clients[:]:  # Copy list to avoid modification during iteration
                    try:
                        client.send(gga_sentence.encode('ascii'))
                        client.send(rmc_sentence.encode('ascii'))
#pylint: disable=W0718
                    except Exception as e:
                        print(f"Error sending to client: {e}")
                        disconnected_clients.append(client)
#pylint: enable=W0718
                # Remove disconnected clients
                for client in disconnected_clients:
                    if client in self.clients:
                        self.clients.remove(client)
                        client.close()

            time.sleep(1)  # Send data every second

    def start(self):
        """Start the NMEA server"""
        self.running = True

        # Create server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"NMEA server started on {self.host}:{self.port}")

            # Start broadcast thread
            broadcast_thread = threading.Thread(target=self.broadcast_data, daemon=True)
            broadcast_thread.start()

            # Accept client connections
            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address),
                        daemon=True
                    )
                    client_thread.start()
#pylint: disable=W0718
                except Exception as e:
                    if self.running:
                        print(f"Error accepting connection: {e}")
#pylint: enable=W0718
#pylint: disable=W0718
        except Exception as e:
            print(f"Server error: {e}")
#pylint: enable=W0718
        finally:
            self.stop()

    def stop(self):
        """Stop the NMEA server"""
        print("Stopping NMEA server...")
        self.running = False

        # Close all client connections
        for client in self.clients[:]:
            client.close()
        self.clients.clear()

        # Close server socket
        if self.server_socket:
            self.server_socket.close()

        print("NMEA server stopped")


def main():
    """Example usage"""
    server = NMEAServer(host='0.0.0.0', port=10110)

    try:
        # Start server in a separate thread
        server_thread = threading.Thread(target=server.start, daemon=True)
        server_thread.start()

        # Simulate position updates (you would get these from your celestial nav calculations)
        while True:
            try:
                # Example: simulate a boat moving around coordinates
                # In your app, you'd call server.update_position() when you have new coordinates
                lat = float(input("Enter latitude (or 'q' to quit): "))
                lon = float(input("Enter longitude: "))
                server.update_position(lat, lon)

            except ValueError:
                print("Invalid coordinates")
            except KeyboardInterrupt:
                break
            except EOFError:
                break

    except KeyboardInterrupt:
        pass
    finally:
        server.stop()


if __name__ == "__main__":
    main()
