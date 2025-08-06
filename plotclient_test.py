#!/usr/bin/env python3
"""
    NMEA 0183 TCP Client for Testing
    Connects to NMEA server and displays received navigation data

    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)     
"""

import socket
import threading
import time
from datetime import datetime

class NMEAClient:
    ''' This is a client for the NMEA 0183 protocol '''
    def __init__(self, host='localhost', port=10110):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        self.buffer = ""

        # Statistics
        self.messages_received = 0
        self.last_position = None
        self.connection_time = None

    def parse_coordinate(self, coord_str, direction):
        """Parse NMEA coordinate format (DDMM.MMMM or DDDMM.MMMM) to decimal degrees"""
        if not coord_str or not direction:
            return None

        try:
            # Handle longitude (DDDMM.MMMM) vs latitude (DDMM.MMMM)
            # if len(coord_str) > 9:  # Longitude format
            if len(coord_str) >= 9: # BUG Correction
                degrees = int(coord_str[:3])
                minutes = float(coord_str[3:])
            else:  # Latitude format
                degrees = int(coord_str[:2])
                minutes = float(coord_str[2:])

            decimal_degrees = degrees + (minutes / 60.0)

            # Apply direction
            if direction in ['S', 'W']:
                decimal_degrees = -decimal_degrees

            return decimal_degrees
        except (ValueError, IndexError):
            return None

    def parse_gga(self, fields):
        """Parse NMEA GGA sentence"""
        try:
            if len(fields) < 15:
                return None

            time_str = fields[1]
            lat_str = fields[2]
            lat_dir = fields[3]
            lon_str = fields[4]
            lon_dir = fields[5]
            fix_quality = fields[6]
            num_satellites = fields[7]
            hdop = fields[8]
            altitude = fields[9]

            latitude = self.parse_coordinate(lat_str, lat_dir)
            longitude = self.parse_coordinate(lon_str, lon_dir)

            if latitude is None or longitude is None:
                return None

            return {
                'type': 'GGA',
                'time': time_str,
                'latitude': latitude,
                'longitude': longitude,
                'fix_quality': int(fix_quality) if fix_quality else 0,
                'satellites': int(num_satellites) if num_satellites else 0,
                'hdop': float(hdop) if hdop else 0.0,
                'altitude': float(altitude) if altitude else 0.0
            }
        except (ValueError, IndexError):
            return None

    def parse_rmc(self, fields):
        """Parse NMEA RMC sentence"""
        try:
            if len(fields) < 13:
                return None

            time_str = fields[1]
            status = fields[2]
            lat_str = fields[3]
            lat_dir = fields[4]
            lon_str = fields[5]
            lon_dir = fields[6]
            speed = fields[7]
            course = fields[8]
            date_str = fields[9]

            if status != 'A':  # A = valid, V = invalid
                return None

            latitude = self.parse_coordinate(lat_str, lat_dir)
            longitude = self.parse_coordinate(lon_str, lon_dir)

            if latitude is None or longitude is None:
                return None

            return {
                'type': 'RMC',
                'time': time_str,
                'date': date_str,
                'latitude': latitude,
                'longitude': longitude,
                'speed': float(speed) if speed else 0.0,
                'course': float(course) if course else 0.0,
                'status': status
            }
        except (ValueError, IndexError):
            return None

    def verify_checksum(self, sentence):
        """Verify NMEA sentence checksum"""
        if '*' not in sentence:
            return False

        try:
            data, checksum = sentence.split('*')
            calculated_checksum = 0
            for char in data[1:]:  # Skip the $
                calculated_checksum ^= ord(char)

            return f"{calculated_checksum:02X}" == checksum.upper()
#pylint: disable=W0702
        except:
            return False
#pylint: enable=W0702

    def parse_nmea_sentence(self, sentence):
        """Parse a complete NMEA sentence"""
        sentence = sentence.strip()

        if not sentence.startswith('$'):
            return None

        # Verify checksum
        if not self.verify_checksum(sentence):
            print(f"⚠️  Checksum error: {sentence}")
            return None

        # Remove checksum for parsing
        if '*' in sentence:
            sentence = sentence.split('*')[0]

        fields = sentence.split(',')
        sentence_type = fields[0][1:]  # Remove $

        if sentence_type.endswith('GGA'):
            return self.parse_gga(fields)
        elif sentence_type.endswith('RMC'):
            return self.parse_rmc(fields)
        else:
            return {'type': sentence_type, 'raw': sentence}

    def format_position(self, lat, lon):
        """Format position for display"""
        lat_dir = 'N' if lat >= 0 else 'S'
        lon_dir = 'E' if lon >= 0 else 'W'

        lat_deg = int(abs(lat))
        lat_min = (abs(lat) - lat_deg) * 60

        lon_deg = int(abs(lon))
        lon_min = (abs(lon) - lon_deg) * 60

        return f"{lat_deg}°{lat_min:06.3f}'{lat_dir} {lon_deg}°{lon_min:06.3f}'{lon_dir}"

    def display_data(self, data):
        """Display parsed NMEA data"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        if data['type'] == 'GGA':
            pos_str = self.format_position(data['latitude'], data['longitude'])
            print(f"\n📍 [{timestamp}] GPS Fix (GGA)")
            print(f"   Position: {pos_str}")
            print(f"   Decimal:  {data['latitude']:.6f}, {data['longitude']:.6f}")
            print(f"   Quality:  {data['fix_quality']} | Satellites: {data['satellites']}")
            print(f"   Altitude: {data['altitude']:.1f}m | HDOP: {data['hdop']:.1f}")

            self.last_position = (data['latitude'], data['longitude'])

        elif data['type'] == 'RMC':
            pos_str = self.format_position(data['latitude'], data['longitude'])
            print(f"\n🧭 [{timestamp}] Navigation (RMC)")
            print(f"   Position: {pos_str}")
            print(f"   Speed:    {data['speed']:.1f} knots")
            print(f"   Course:   {data['course']:.1f}°")
            print(f"   Time:     {data['time']} | Date: {data['date']}")

        else:
            print(f"\n📡 [{timestamp}] {data['type']}: {data.get('raw', 'Unknown')}")

    def receive_data(self):
        """Receive and process NMEA data"""
        while self.running:
            try:
                assert self.socket is not None
                data = self.socket.recv(1024).decode('ascii', errors='ignore')
                if not data:
                    print("❌ Connection closed by server")
                    break

                self.buffer += data

                # Process complete lines
                while '\n' in self.buffer:
                    line, self.buffer = self.buffer.split('\n', 1)
                    line = line.strip()

                    if line:
                        self.messages_received += 1
                        parsed = self.parse_nmea_sentence(line)
                        if parsed:
                            self.display_data(parsed)

            except socket.timeout:
                continue
#pylint: disable=W0718
            except Exception as e:
                if self.running:
                    print(f"❌ Receive error: {e}")
                break
#pylint: enable=W0718

    def connect(self):
        """Connect to NMEA server"""
        try:
            print(f"🔌 Connecting to NMEA server at {self.host}:{self.port}...")

            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0)
            self.socket.connect((self.host, self.port))

#pylint: disable=W1309
            print(f"✅ Connected successfully!")
            print(f"📊 Listening for NMEA data... (Press Ctrl+C to quit)")
#pylint: enable=W1309
            print("=" * 60)

            self.running = True
            self.connection_time = datetime.now()

            # Start receiving data
            receive_thread = threading.Thread(target=self.receive_data, daemon=True)
            receive_thread.start()

            # Keep main thread alive and show status
            try:
                while self.running:
                    time.sleep(10)
                    uptime = datetime.now() - self.connection_time
                    print\
                    (f"\n📈 Status: {self.messages_received} messages received | Uptime: {uptime}")
                    if self.last_position:
                        pos_str = self.format_position(*self.last_position)
                        print(f"📍 Last position: {pos_str}")

            except KeyboardInterrupt:
                print("\n🛑 Disconnecting...")

        except socket.timeout:
            print(f"❌ Connection timeout - is the server running on {self.host}:{self.port}?")
        except ConnectionRefusedError:
            print(f"❌ Connection refused - is the server running on {self.host}:{self.port}?")
#pylint: disable=W0718
        except Exception as e:
            print(f"❌ Connection error: {e}")
#pylint: enable=W0718
        finally:
            self.disconnect()

    def disconnect(self):
        """Disconnect from server"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
#pylint: disable=W0702
            except:
                pass
#pylint: enable=W0702

        if self.connection_time:
            uptime = datetime.now() - self.connection_time
            print(f"📊 Session complete: {self.messages_received} messages in {uptime}")


def main(host = None):
    """Main function with command line interface"""
#pylint: disable=C0415
    import sys
#pylint: enable=C0415

    # Default connection parameters

    if host is None:
        host = '192.168.0.241'
    else:
        host = sys.argv[1:]
    assert isinstance (host, str)

    port = 10110

    # Parse command line arguments
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("❌ Invalid port number")
            sys.exit(1)

    print("🌊 NMEA 0183 Test Client")
    print(f"Target: {host}:{port}")
    print("Usage: python nmea_client.py [host] [port]")
    print("=" * 50)

    client = NMEAClient(host, port)
    client.connect()


if __name__ == "__main__":
    main()
