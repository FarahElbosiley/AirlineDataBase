import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

def connect_db():
    """Establish a connection to the database."""
    return mysql.connector.connect(host = "localhost",user="root",passwd = "1234",database = "NewAirline")
def is_entry_valid(entry):
    # Basic validation function to ensure the entry is not empty
    return entry.get().strip() != ""
class AirlineApp(tk.Tk):
    def __init__(self, root):
        self.root = root
        self.root.title("Airline Management System")
        self.root.geometry("900x500")  # Set the main window size

        # Setup the notebook (tab control)
        self.tabControl = ttk.Notebook(self.root)

        # Initialize all tabs
        self.setup_flights_tab()  # Set up the Flights tab
        self.setup_aircrafts_tab()  # Set up the Aircrafts tab
        self.setup_airlines_tab()  # Set up the Airlines tab
        self.setup_crew_tab()  # Set up the Crew Members tab
        self.setup_passengers_tab()
        self.setup_reservations_tab()
        self.setup_airport_tab()
        self.setup_payments_tab()
        self.setup_tickets_tab()
        self.tabControl.pack(expand=1, fill="both")

    def setup_airport_tab(self):
        self.airport_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.airport_tab, text='Airports')

        # Labels and Entries for airports details

        ttk.Label(self.airport_tab, text='Airport Name:').grid(row=1, column=0, padx=10, pady=5)
        self.airport_name_entry = ttk.Entry(self.airport_tab)
        self.airport_name_entry.grid(row=1, column=1, sticky="nsew")

        ttk.Label(self.airport_tab, text='Country:').grid(row=2, column=0, padx=10, pady=5)
        self.country_entry = ttk.Entry(self.airport_tab)
        self.country_entry.grid(row=2, column=1, sticky="nsew")

        ttk.Label(self.airport_tab, text='Website:').grid(row=3, column=0, padx=10, pady=5)
        self.website_entry = ttk.Entry(self.airport_tab)
        self.website_entry.grid(row=3, column=1, sticky="nsew")

        # Buttons for managing airlines
        ttk.Button(self.airport_tab, text='Add Airport', command=self.add_airport, width=5).grid(row=4, column=0,
                                                                                                        pady=10,
                                                                                                        sticky="nsew")
        ttk.Button(self.airport_tab, text='View Airports', command=self.view_airports, width=5).grid(row=4,
                                                                                                            column=1,
                                                                                                            pady=10,
                                                                                                            sticky="nsew")
        ttk.Button(self.airport_tab, text='Delete Airport', command=self.delete_selected_airport, width=5).grid(
            row=4,
            column=2,
            pady=10,
            sticky="ew")

        # Treeview for displaying airports
        self.airport_tree = ttk.Treeview(self.airport_tab, columns=("Airport Name", "Country", "Website"), show="headings")
        self.airport_tree.grid(row=5, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        # Set headings for the columns
        for col in self.airport_tree["columns"]:
            self.airport_tree.heading(col, text=col)
            self.airport_tree.column(col, anchor=tk.CENTER)

        # Scrollbar for the Treeview
        self.airport_scroll = ttk.Scrollbar(self.airport_tab, orient="vertical",
                                              command=self.airport_tree.yview)
        self.airport_scroll.grid(row=5, column=3, sticky='nsew')
        self.airport_tree.configure(yscrollcommand=self.airport_scroll.set)

    def add_airport(self):
        entries = [self.airport_name_entry, self.country_entry,
                   self.website_entry]
        if not all(is_entry_valid(entry) for entry in entries):
            messagebox.showerror("Error", "All fields must be filled out.")
            return
        airport_name = self.airport_name_entry.get()
        country = self.country_entry.get()
        website = self.website_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""INSERT INTO Airports (airport_name, country, website)
                                      VALUES (%s, %s, %s, %s, %s)""",
                           (airport_name, country, website))
            conn.commit()
            messagebox.showinfo("Success", "Airport added successfully")
        except Exception as e:
            messagebox.showerror("Error", "Failed to add airport")
            print(e)
        finally:
            conn.close()
        self.view_airport()

    def view_airports(self):

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT airport_name, country, website FROM Airports")
            rows = cursor.fetchall()
            self.airport_tree.delete(*self.airport_tree.get_children())  # Clear the current view
            for row in rows:
                self.airport_tree.insert("", tk.END, values=row)  # Insert new data
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh airports: {e}")
        finally:
            conn.close()

    def delete_selected_airport(self):
        """Delete the selected airport from the database."""
        selected_items = self.airport_tree.selection()  # Gets the list of all selected items
        if selected_items:
            selected_item = selected_items[0]  # Assuming single selection, gets the first item
            airport_id = self.airport_tree.item(selected_item, 'values')[
                1]  # Get airport id from the second column

            response = messagebox.askyesno("Confirm", "Are you sure you want to delete this airport?")
            if response:
                conn = connect_db()
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM Airports WHERE airport_id=%s", (airport_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Airport deleted successfully")
                    self.view_airports()  # Refresh the list after deletion
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete airport: {e}")
                finally:
                    conn.close()
        else:
            messagebox.showerror("Error", "No Airports selected for deletion.")

    def setup_payments_tab(self):
        self.payment_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.payment_tab, text='Payments')

        # Labels and Entries for payment details
        ttk.Label(self.payment_tab, text='Payment Method:').grid(row=1, column=0, padx=10, pady=5)
        self.payment_method_entry = ttk.Entry(self.payment_tab)
        self.payment_method_entry.grid(row=1, column=1, sticky="nsew")

        ttk.Label(self.payment_tab, text='Payment Amount:').grid(row=2, column=0, padx=10, pady=5)
        self.amount_entry = ttk.Entry(self.payment_tab)
        self.amount_entry.grid(row=2, column=1, sticky="nsew")

        ttk.Label(self.payment_tab, text='Payment Date:').grid(row=3, column=0, padx=10, pady=5)
        self.date_entry = ttk.Entry(self.payment_tab)
        self.date_entry.grid(row=3, column=1, sticky="nsew")

        # Buttons for managing payments
        ttk.Button(self.payment_tab, text='Add Payment', command=self.add_payment, width=5).grid(row=4, column=0,
                                                                                                 pady=10,
                                                                                                 sticky="nsew")
        ttk.Button(self.payment_tab, text='View Payments', command=self.refresh_payments, width=5).grid(row=4,
                                                                                                     column=1,
                                                                                                     pady=10,
                                                                                                     sticky="nsew")
        ttk.Button(self.payment_tab, text='Delete Payment', command=self.delete_selected_payment, width=5).grid(
            row=4,
            column=2,
            pady=10,
            sticky="ew")

        # Treeview for displaying payments
        self.payment_tree = ttk.Treeview(self.payment_tab, columns=("Payment Method", "Payment Amount", "Payment Date"), show="headings")
        self.payment_tree.grid(row=5, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        # Set headings for the columns
        for col in self.payment_tree["columns"]:
            self.payment_tree.heading(col, text=col)
            self.payment_tree.column(col, anchor=tk.CENTER)

        # Scrollbar for the Treeview
        self.payment_scroll = ttk.Scrollbar(self.payment_tab, orient="vertical",
                                            command=self.payment_tree.yview)
        self.payment_scroll.grid(row=5, column=3, sticky='nsew')
        self.payment_tree.configure(yscrollcommand=self.payment_scroll.set)

    def add_payment(self):
        payment_method = self.payment_mathod_entry.get().strip()

        payment_amount = self.payment_amount_entry.get().strip()
        payment_date = self.payment_date_entry.get().strip()

        if is_entry_valid(self.payment_method_entry) and is_entry_valid(self.payment_amount_entry) and \
                is_entry_valid(self.payment_date_entry):
            conn = connect_db()
            cursor = conn.cursor()

            # Insert the payment into the database
            cursor.execute(
                "INSERT INTO Payment (payment_method,payment_amount, payment_date, ) VALUES (?, datetime('now'), ?)",
                (payment_amount, payment_method))
            conn.commit()

            # Clear the entry fields
            self.payment_method_entry.delete(0, tk.END)

            self.payment_amount_entry.delete(0, tk.END)
            self.payment_date_entry.delete(0, tk.END)

            # Refresh the payments list
            self.refresh_payments()

            conn.close()

    def refresh_payments(self):
        # Clear existing data from the treeview
        self.payments_tree.delete(*self.payments_tree.get_children())

        conn = connect_db()
        cursor = conn.cursor()

        # Retrieve payments from the database
        cursor.execute("SELECT * FROM Payment")
        payments = cursor.fetchall()

        # Populate the treeview with payment data
        for payment in payments:
            self.payments_tree.insert("", tk.END, values=payment)

        conn.close()

    def delete_selected_payment(self):
        selected_item = self.payments_tree.selection()
        if selected_item:
            conn = connect_db()
            cursor = conn.cursor()

            # Get the payment ID of the selected payment
            payment_id = self.payments_tree.item(selected_item)["values"][0]

            # Delete the payment from the database
            cursor.execute("DELETE FROM Payment WHERE payment_id=?", (payment_id,))
            conn.commit()

            # Refresh the payments list
            self.refresh_payments()

            conn.close()

    def setup_tickets_tab(self):
        self.tickets_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tickets_tab, text='Tickets')

        # Labels and Entries for ticket details
        ttk.Label(self.tickets_tab, text='Ticket Type:').grid(row=0, column=0, padx=10, pady=5)
        self.ticket_type_entry = ttk.Entry(self.tickets_tab)
        self.ticket_type_entry.grid(row=0, column=1, sticky="nsew")

        ttk.Label(self.tickets_tab, text='Price:').grid(row=1, column=0, padx=10, pady=5)
        self.price_entry = ttk.Entry(self.tickets_tab)
        self.price_entry.grid(row=1, column=1, sticky="nsew")

        ttk.Label(self.tickets_tab, text='Seat Number:').grid(row=2, column=0, padx=10, pady=5)
        self.seat_number_entry = ttk.Entry(self.tickets_tab)
        self.seat_number_entry.grid(row=2, column=1, sticky="nsew")

        ttk.Button(self.tickets_tab, text="Add Ticket", command=self.add_ticket, width=5).grid(row=3, column=0,
                                                                                               pady=10,
                                                                                               sticky="ew")
        # Displaying tickets
        self.tickets_tree = ttk.Treeview(self.tickets_tab, columns=(
            "Ticket ID", "Ticket Type", "Price", "Seat Number"), show="headings")
        self.tickets_tree.grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
        for col in self.tickets_tree["columns"]:
            self.tickets_tree.heading(col, text=col)
            self.tickets_tree.column(col, anchor=tk.CENTER)
            self.tickets_tree.column(col, width=150)  # Adjust the width as needed

        ttk.Button(self.tickets_tab, text="Refresh Tickets", command=self.refresh_tickets, width=5).grid(row=3, column=1,
                                                                                                pady=10,
                                                                                                sticky="ew")

        ttk.Button(self.tickets_tab, text='Delete Ticket', command=self.delete_selected_ticket, width=5).grid(row=3, column=2,
                                                                                                     pady=10,
                                                                                                     sticky="ew")

    def add_ticket(self):
        ticket_type = self.ticket_type_entry.get().strip()
        price = self.price_entry.get().strip()
        seat_number = self.seat_number_entry.get().strip()

        if is_entry_valid(self.ticket_type_entry) and is_entry_valid(self.price_entry) and is_entry_valid(
                self.seat_number_entry):
            conn = connect_db()
            cursor = conn.cursor()

            # Insert the ticket into the database
            cursor.execute("INSERT INTO Tickets (ticket_type, price, seat_number) VALUES (?, ?, ?)",
                            (ticket_type, price, seat_number))
            conn.commit()

            # Clear the entry fields
            self.ticket_type_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.seat_number_entry.delete(0, tk.END)

            # Refresh the tickets list
            self.refresh_tickets()

            conn.close()

    def refresh_tickets(self):
        # Clear existing data from the treeview
        self.tickets_tree.delete(*self.tickets_tree.get_children())

        conn = connect_db()
        cursor = conn.cursor()

        # Retrieve tickets from the database
        cursor.execute("SELECT * FROM Tickets")
        tickets = cursor.fetchall()

        # Populate the treeview with ticket data
        for ticket in tickets:
            self.tickets_tree.insert("", tk.END, values=ticket)

        conn.close()

    def delete_selected_ticket(self):
        selected_item = self.tickets_tree.selection()
        if selected_item:
            conn = connect_db()
            cursor = conn.cursor()

            # Get the ticket ID of the selected ticket
            ticket_id = self.tickets_tree.item(selected_item)["values"][0]

            # Delete the ticket from the database
            cursor.execute("DELETE FROM Tickets WHERE ticket_id=?", (ticket_id,))
            conn.commit()

            # Refresh the tickets list
            self.refresh_tickets()

            conn.close()

    def setup_reservations_tab(self):
        self.reservations_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.reservations_tab, text='Reservations')

        # UI for adding a booking
        ttk.Label(self.reservations_tab, text="Flight ID:").grid(row=0, column=0, padx=10, pady=5)
        self.flight_id_entry = ttk.Entry(self.reservations_tab)
        self.flight_id_entry.grid(row=0, column=1, sticky= "nsew")

        ttk.Label(self.reservations_tab, text="Passenger ID:").grid(row=1, column=0, padx=10, pady=5)
        self.passenger_id_entry = ttk.Entry(self.reservations_tab)
        self.passenger_id_entry.grid(row=1, column=1,sticky= "nsew")

        ttk.Button(self.reservations_tab, text="Add Booking", command=self.add_booking,width=5).grid(row=2, column=0,
                                                                                                        pady=10,
                                                                                                        sticky="ew")

        # Displaying bookings
        self.bookings_tree = ttk.Treeview(self.reservations_tab, columns=(
            "Booking ID", "Flight ID", "Passenger ID", "Booking Date"), show="headings")
        self.bookings_tree.grid(row=3, column=0, columnspan=2, sticky="nsew")
        for col in self.bookings_tree["columns"]:
            self.bookings_tree.heading(col, text=col)
            self.bookings_tree.column(col, anchor=tk.CENTER)
            self.bookings_tree.column(col, width=150)  # Adjust the width as needed

        ttk.Button(self.reservations_tab, text="View Bookings", command=self.refresh_bookings,width=5).grid(row=2,
                                                                                                               column=1,
                                                                                                               pady=10,
                                                                                                            sticky="ew")
        ttk.Button(self.reservations_tab, text='Delete Booking', command=self.delete_selected_booking,width=50).grid(row=2,
                                                                                                            column=2,
                                                                                                            pady=10,
                                                                                                            sticky="ew")


    def add_booking(self):
        entries = [self.flight_id_entry, self.passenger_id_entry]
        if not all(is_entry_valid(entry) for entry in entries):
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        flight_id = self.flight_id_entry.get().strip()
        passenger_id = self.passenger_id_entry.get().strip()

        booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Booking date as current datetime

        conn = connect_db()
        cursor = conn.cursor()
        try:
            # Check if the flight exists
            cursor.execute("SELECT * FROM Flights WHERE flight_id=%s", (flight_id,))
            if not cursor.fetchone():
                messagebox.showerror("Error", "Flight ID does not exist.")
                return

            # Check if the passenger exists
            cursor.execute("SELECT * FROM Passengers WHERE passenger_id=%s", (passenger_id,))
            if not cursor.fetchone():
                messagebox.showerror("Error", "Passenger ID does not exist.")
                return

            query = "INSERT INTO Bookings (flight_id, passenger_id, booking_date) VALUES (%s, %s, %s)"
            cursor.execute(query, (flight_id, passenger_id, booking_date))
            conn.commit()
            messagebox.showinfo("Success", "Booking successfully added!")
        #except sqlite3.IntegrityError:
            #messagebox.showerror("Error", "Booking could not be added. Please check flight and passenger IDs.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add booking: {e}")
        finally:
            conn.close()
        self.refresh_bookings()



    def refresh_bookings(self):
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT booking_id, flight_id, passenger_id, booking_date FROM Bookings")
            rows = cursor.fetchall()
            self.bookings_tree.delete(*self.bookings_tree.get_children())  # Clear the current view
            for row in rows:
                self.bookings_tree.insert("", tk.END, values=row)  # Insert new data
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh bookings: {e}")
        finally:
            conn.close()

    def setup_flights_tab(self):
        self.flights_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.flights_tab, text='Flights')

        # Labels and Entries for flight details
        ttk.Label(self.flights_tab, text='Flight Number:').grid(row=0, column=0, padx=10, pady=5)
        self.flight_number_entry = ttk.Entry(self.flights_tab)
        self.flight_number_entry.grid(row=0, column=1,sticky= "nsew")

        ttk.Label(self.flights_tab, text='Departure City:').grid(row=1, column=0,padx=10, pady=5)
        self.departure_city_entry = ttk.Entry(self.flights_tab)
        self.departure_city_entry.grid(row=1, column=1,sticky= "nsew")

        ttk.Label(self.flights_tab, text='Arrival City:').grid(row=2, column=0,padx=10, pady=5)
        self.arrival_city_entry = ttk.Entry(self.flights_tab)
        self.arrival_city_entry.grid(row=2, column=1,sticky= "nsew")

        ttk.Label(self.flights_tab, text='Departure Time:').grid(row=3, column=0,padx=10, pady=5)
        self.departure_time_entry = ttk.Entry(self.flights_tab)
        self.departure_time_entry.grid(row=3, column=1,sticky= "nsew")

        ttk.Label(self.flights_tab, text='Arrival Time:').grid(row=4, column=0,padx=10, pady=5)
        self.arrival_time_entry = ttk.Entry(self.flights_tab)
        self.arrival_time_entry.grid(row=4, column=1,sticky= "nsew")

        # Buttons for managing flights
        ttk.Button(self.flights_tab, text='Add Flight', command=self.add_flight, width=3).grid(row=5,
                                                                                                column=0,
                                                                                                pady=10,
                                                                                                sticky="ew")
        ttk.Button(self.flights_tab, text='View Flights', command=self.view_flights,  width=3).grid(row=5,
                                                                                                              column=1,
                                                                                                              pady=10,
                                                                                                              sticky="ew")
        ttk.Button(self.flights_tab, text='Delete Selected Flight', command=self.delete_flight,  width= 5).grid(row=5,
                                                                                                              column=2,
                                                                                                              pady=10,
                                                                                                              sticky="ew")
        ttk.Button(self.flights_tab, text='Edit Selected Flight', command=self.load_flight_data, width= 5).grid(row=5,
                                                                                                              column=3,
                                                                                                              pady=10,
                                                                                                              sticky="ew")
        ttk.Button(self.flights_tab, text='Update Flight', command=self.update_flight,width= 5).grid(row=6,
                                                                                                    column=1,
                                                                                                    pady=10,
                                                                                                    sticky="ew")
        # Treeview for displaying flights
        self.flights_tree = ttk.Treeview(self.flights_tab, columns=(
            "Flight ID", "Flight Number", "Departure City", "Arrival City", "Departure Time", "Arrival Time"),
                                        show="headings")
        self.flights_tree.grid(row=7, column=0, columnspan=4, pady=10, padx=10)
        for col in self.flights_tree["columns"]:
            self.flights_tree.heading(col, text=col)
            self.flights_tree.column(col, anchor=tk.CENTER)
            self.flights_tree.column(col, width=150)  # Adjust the width as needed

        self.flights_tree.grid(row=7, column=0, columnspan=4, pady=10, padx=10)

    def load_flight_data(self):
        selected_item = self.flights_tree.selection()
        if selected_item:  # Check if something is actually selected
            flight_details = self.flights_tree.item(selected_item, "values")
            self.flight_number_entry.delete(0, tk.END)
            self.flight_number_entry.insert(0, flight_details[1])
            self.departure_city_entry.delete(0, tk.END)
            self.departure_city_entry.insert(0, flight_details[2])
            self.arrival_city_entry.delete(0, tk.END)
            self.arrival_city_entry.insert(0, flight_details[3])
            self.departure_time_entry.delete(0, tk.END)
            self.departure_time_entry.insert(0, flight_details[4])
            self.arrival_time_entry.delete(0, tk.END)
            self.arrival_time_entry.insert(0, flight_details[5])
            self.edit_flight_id = flight_details[0]  # Save flight ID for updating

        else:
            messagebox.showerror("Error", "No flight selected for editing.")

    def update_flight(self):
        if hasattr(self, 'edit_flight_id'):
            flight_id = self.edit_flight_id
            flight_number = self.flight_number_entry.get()
            departure_city = self.departure_city_entry.get()
            arrival_city = self.arrival_city_entry.get()
            departure_time = self.departure_time_entry.get()
            arrival_time = self.arrival_time_entry.get()

            conn = connect_db()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """UPDATE Flights SET flight_number=%s, departure_city=%s, arrival_city=%s, departure_time=%s, arrival_time=%s WHERE flight_id=%s""",
                    (flight_number, departure_city, arrival_city, departure_time, arrival_time, flight_id))
                conn.commit()
                messagebox.showinfo("Success", "Flight updated successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update flight: {e}")
            finally:
                conn.close()
            self.view_flights()  # Refresh the flight list
        else:
            messagebox.showerror("Error", "No flight loaded for updating.")

    def setup_airlines_tab(self):
        self.airlines_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.airlines_tab, text='Airlines')

        # Define Labels and Entries for airline details
        ttk.Label(self.airlines_tab, text='Airline Name:').grid(row=0, column=0, padx=10, pady=5)
        self.airline_name_entry = ttk.Entry(self.airlines_tab)
        self.airline_name_entry.grid(row=0, column=1, sticky="nsew")

        ttk.Label(self.airlines_tab, text='Country:').grid(row=1, column=0, padx=10, pady=5)
        self.airline_country_entry = ttk.Entry(self.airlines_tab)
        self.airline_country_entry.grid(row=1, column=1, sticky="nsew")

        ttk.Label(self.airlines_tab, text='Website:').grid(row=2, column=0, padx=10, pady=5)
        self.airline_website_entry = ttk.Entry(self.airlines_tab)
        self.airline_website_entry.grid(row=2, column=1, sticky="nsew")

        # Buttons for managing airlines
        ttk.Button(self.airlines_tab, text='Add Airline', command=self.add_airline, width=5).grid(row=3,
                                                                                                  column=0,
                                                                                                  pady=10,
                                                                                                  sticky="ew")
        ttk.Button(self.airlines_tab, text='View Airlines', command=self.view_airlines, width=5).grid(row=3,
                                                                                                      column=1,
                                                                                                      pady=10,
                                                                                                      sticky="ew")
        ttk.Button(self.airlines_tab, text='Delete Airline', command=self.delete_selected_airline, width=5).grid(row=3,
                                                                                                                 column=2,
                                                                                                                 pady=10,
                                                                                                                 sticky="ew")

        self.airlines_tree = ttk.Treeview(self.airlines_tab, columns=("Airline ID", "Airline Name", "Country",
                                                                      "Website", "Total Flights"),
                                          show="headings")
        self.airlines_tree.grid(row=4, column=0, columnspan=3, sticky='ew', padx=10, pady=10)

        # Set headings and column configurations
        for col in self.airlines_tree["columns"]:
            self.airlines_tree.heading(col, text=col)
            self.airlines_tree.column(col, anchor=tk.CENTER, width=150)

        # Fetch data from the database and populate the Treeview
        self.populate_treeview()

    def populate_treeview(self):
        conn = connect_db()
        cursor = conn.cursor()
        # Execute SQL query to fetch data from the view
        cursor.execute("SELECT * FROM AirlinesWithTotalFlights")

        # Clear existing items in the Treeview
        self.airlines_tree.delete(*self.airlines_tree.get_children())

        # Populate the Treeview with fetched data
        for row in cursor.fetchall():
            self.airlines_tree.insert("", "end", values=row)

        # Close the database connection
        cursor.close()
        conn.close()

    def setup_crew_tab(self):
        self.crew_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.crew_tab, text='Crew Members')

        # Define Labels and Entries for crew member details
        ttk.Label(self.crew_tab, text='First Name:').grid(row=0, column=0, padx=10, pady=5)
        self.first_name_entry = ttk.Entry(self.crew_tab)
        self.first_name_entry.grid(row=0, column=1,sticky= "nsew")

        ttk.Label(self.crew_tab, text='Last Name:').grid(row=1, column=0,padx=10, pady=5)
        self.last_name_entry = ttk.Entry(self.crew_tab)
        self.last_name_entry.grid(row=1, column=1,sticky= "nsew")

        ttk.Label(self.crew_tab, text='Position:').grid(row=2, column=0,padx=10, pady=5)
        self.position_entry = ttk.Entry(self.crew_tab)
        self.position_entry.grid(row=2, column=1,sticky= "nsew")

        ttk.Label(self.crew_tab, text='Experience (Years):').grid(row=3, column=0,padx=10, pady=5)
        self.experience_entry = ttk.Entry(self.crew_tab)
        self.experience_entry.grid(row=3, column=1,sticky= "nsew")

        # Buttons for managing crew members
        ttk.Button(self.crew_tab, text='Add Crew Member', command=self.add_crew_member, width= 5).grid(row=4,
                                                                                                    column=0,
                                                                                                    pady=10,
                                                                                                    sticky="ew")
        ttk.Button(self.crew_tab, text='View Crew', command=self.view_crew, width= 5).grid(row=4,
                                                                                                    column=1,
                                                                                                    pady=10,
                                                                                                    sticky="ew")
        ttk.Button(self.crew_tab, text='Delete Crew Member', command=self.delete_selected_crew_member, width= 5).grid(row=4,
                                                                                                    column=2,
                                                                                                    pady=10,
                                                                                                    sticky="ew")


        # Treeview for displaying crew members
        self.crew_tree = ttk.Treeview(self.crew_tab, columns=(
            "Crew ID", "First Name", "Last Name", "Position", "Experience"), show="headings")
        self.crew_tree.grid(row=5, column=0, columnspan=3, sticky='ew', padx=10, pady=10)
        for col in self.crew_tree["columns"]:
            self.crew_tree.heading(col, text=col)
            self.crew_tree.column(col, anchor=tk.CENTER)
            self.crew_tree.column(col, width=150)  # Adjust the width as needed

    def add_flight(self):
            # Fetching entries after validation
        entries = [self.flight_number_entry, self.departure_city_entry, self.arrival_city_entry,
                   self.departure_time_entry, self.arrival_time_entry]
        if not all(is_entry_valid(entry) for entry in entries):
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        flight_number = self.flight_number_entry.get().strip()
        departure_city = self.departure_city_entry.get().strip()
        arrival_city = self.arrival_city_entry.get().strip()
        departure_time = self.departure_time_entry.get().strip()
        arrival_time = self.arrival_time_entry.get().strip()


        conn = connect_db()
        cursor = conn.cursor()
        try:
            # Check if the flight number already exists
            cursor.execute("SELECT * FROM Flights WHERE flight_number=%s", (flight_number,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Flight number already exists. Please use a unique flight number.")
                return  # Stop the function if the flight number is not unique

            # Proceed with adding the new flight
            cursor.execute("""INSERT INTO Flights (flight_number, departure_city, arrival_city, departure_time, arrival_time)
                              VALUES (%s, %s, %s, %s, %s)""",
                           (flight_number, departure_city, arrival_city, departure_time, arrival_time))
            conn.commit()
            messagebox.showinfo("Success", "Flight added successfully")
        except Exception as e:
            messagebox.showerror("Error", "Failed to add flight")
            print(e)
        finally:
            conn.close()
        self.view_flights()  # Update the view automatically

    def view_flights(self):
        """Fetch and display flights from the database."""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT flight_id, flight_number, departure_city, arrival_city, departure_time, arrival_time FROM Flights")
            rows = cursor.fetchall()
            self.flights_tree.delete(*self.flights_tree.get_children())  # Clear existing entries
            for row in rows:
                self.flights_tree.insert("", tk.END, values=row)  # Insert new entries with IDs
        except Exception as e:
            messagebox.showerror("Error", "Failed to fetch flights")
            print(e)
        finally:
            conn.close()

    def delete_flight(self):
        """Delete the selected flight from the database."""
        selected_items = self.flights_tree.selection()  # Gets the list of all selected items
        if selected_items:
            selected_item = selected_items[0]  # Assuming single selection, gets the first item
            flight_number = self.flights_tree.item(selected_item, 'values')[
                1]  # Get flight number from the second column

            response = messagebox.askyesno("Confirm", "Are you sure you want to delete this flight?")
            if response:
                conn = connect_db()
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM Flights WHERE flight_number=%s", (flight_number,))
                    conn.commit()
                    messagebox.showinfo("Success", "Flight deleted successfully")
                    self.view_flights()  # Refresh the list after deletion
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete flight: {e}")
                finally:
                    conn.close()
        else:
            messagebox.showerror("Error", "No flight selected for deletion.")

    def add_aircraft(self):
        entries = [self.registration_number_entry, self.aircraft_type_entry, self.capacity_entry, self.airline_id_entry, self.airport_id_entry]
        if not all(is_entry_valid(entry) for entry in entries):
            messagebox.showerror("Error", "All fields must be filled out.")
            return
        registration_number = self.registration_number_entry.get()
        aircraft_type = self.aircraft_type_entry.get()
        capacity = self.capacity_entry.get()
        airline_id = self.airline_id_entry.get()
        airport_id = self.airport_id_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""INSERT INTO Aircrafts (registration_number, aircraft_type, capacity, airline_id, airport_id)
                              VALUES (%s, %s, %s, %s, %s)""",
                           (registration_number, aircraft_type, capacity, airline_id, airport_id))
            conn.commit()
            messagebox.showinfo("Success", "Aircraft added successfully")
        except Exception as e:
            messagebox.showerror("Error", "Failed to add aircraft")
            print(e)
        finally:
            conn.close()
        self.view_aircraft()

    def setup_passengers_tab(self):
        self.passengers_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.passengers_tab, text='Passengers')

        # Labels and Entries for passenger details
        ttk.Label(self.passengers_tab, text='First Name:').grid(row=0, column=0, padx=10, pady=5)
        self.first_name_entry = ttk.Entry(self.passengers_tab)
        self.first_name_entry.grid(row=0, column=1, sticky="nsew")

        ttk.Label(self.passengers_tab, text='Last Name:').grid(row=1, column=0, padx=10, pady=5)
        self.last_name_entry = ttk.Entry(self.passengers_tab)
        self.last_name_entry.grid(row=1, column=1, sticky="nsew")

        ttk.Label(self.passengers_tab, text='Phone Number:').grid(row=2, column=0, padx=10, pady=5)
        self.phone_number_entry = ttk.Entry(self.passengers_tab)
        self.phone_number_entry.grid(row=2, column=1, sticky="nsew")

        ttk.Label(self.passengers_tab, text='Email:').grid(row=3, column=0, padx=10, pady=5)
        self.email_entry = ttk.Entry(self.passengers_tab)
        self.email_entry.grid(row=3, column=1, sticky="nsew")

        # Buttons for managing passengers
        ttk.Button(self.passengers_tab, text='Add Passenger', command=self.add_passenger, width=5).grid(row=4, column=0,
                                                                                                        pady=10,
                                                                                                        sticky="nsew")
        ttk.Button(self.passengers_tab, text='View Passengers', command=self.view_passengers, width=5).grid(row=4,
                                                                                                            column=1,
                                                                                                            pady=10,
                                                                                                            sticky="nsew")
        ttk.Button(self.passengers_tab, text='Delete Passenger', command=self.delete_selected_passenger, width=5).grid(
            row=4,
            column=2,
            pady=10,
            sticky="ew")

        # Treeview for displaying passengers
        self.passengers_tree = ttk.Treeview(self.passengers_tab, columns=(
            "Passenger ID", "First Name", "Last Name", "Phone Number", "Email"), show="headings")
        self.passengers_tree.grid(row=5, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
        for col in self.passengers_tree["columns"]:
            self.passengers_tree.heading(col, text=col)
            self.passengers_tree.column(col, anchor=tk.CENTER)
            self.passengers_tree.column(col, width=150)  # Adjust the width as needed

        # Scrollbar for the Treeview
        self.passenger_scroll = ttk.Scrollbar(self.passengers_tab, orient="vertical",
                                              command=self.passengers_tree.yview)
        self.passenger_scroll.grid(row=5, column=3, sticky='nsew')
        self.passengers_tree.configure(yscrollcommand=self.passenger_scroll.set)

    def setup_aircrafts_tab(self):
        self.aircrafts_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.aircrafts_tab, text='Aircrafts')

        # Labels and Entries for aircraft details
        ttk.Label(self.aircrafts_tab, text='Registration Number:').grid(row=0, column=0, padx=10, pady=5)
        self.registration_number_entry = ttk.Entry(self.aircrafts_tab)
        self.registration_number_entry.grid(row=0, column=1,sticky= "nsew")

        ttk.Label(self.aircrafts_tab, text='Aircraft Type:').grid(row=1, column=0,padx=10, pady=5)
        self.aircraft_type_entry = ttk.Entry(self.aircrafts_tab)
        self.aircraft_type_entry.grid(row=1, column=1,sticky= "nsew")

        ttk.Label(self.aircrafts_tab, text='Capacity:').grid(row=2, column=0,padx=10, pady=5)
        self.capacity_entry = ttk.Entry(self.aircrafts_tab)
        self.capacity_entry.grid(row=2, column=1,sticky= "nsew")

        ttk.Label(self.aircrafts_tab, text='Airline ID:').grid(row=3, column=0,padx=10, pady=5)
        self.airline_id_entry = ttk.Entry(self.aircrafts_tab)
        self.airline_id_entry.grid(row=3, column=1, sticky= "nsew")

        ttk.Label(self.aircrafts_tab, text='Airport ID:').grid(row=4, column=0,padx=10, pady=5)
        self.airport_id_entry = ttk.Entry(self.aircrafts_tab)
        self.airport_id_entry.grid(row=4, column=1,sticky= "nsew")

        # Buttons for managing aircraft
        ttk.Button(self.aircrafts_tab, text='Add Aircraft', command=self.add_aircraft, width=5).grid(row=5,
                                                                                                    column=0,
                                                                                                    pady=10,
                                                                                                    sticky="ew")
        ttk.Button(self.aircrafts_tab, text='View Aircraft', command=self.view_aircraft, width=5).grid(row=5,
                                                                                                    column=1,
                                                                                                    pady=10,
                                                                                                    sticky="ew")
        ttk.Button(self.aircrafts_tab, text='Delete Aircraft', command=self.delete_selected_aircraft, width= 5).grid(row=5,
                                                                                                    column=2,
                                                                                                    pady=10,
                                                                                                    sticky="ew")
        # Treeview for displaying aircraft
        self.aircraft_tree = ttk.Treeview(self.aircrafts_tab, columns=(
            "Aircraft ID", "Registration Number", "Aircraft Type", "Capacity", "Airline ID", "Airport ID"),
                                          show="headings")
        self.aircraft_tree.grid(row=6, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")
        for col in self.aircraft_tree["columns"]:
            self.aircraft_tree.heading(col, text=col)
            self.aircraft_tree.column(col, anchor=tk.CENTER)
            self.aircraft_tree.column(col, width=80)  # Adjust the width as needed

        # Scrollbar for the Treeview
        self.aircraft_scroll = ttk.Scrollbar(self.aircrafts_tab, orient="vertical",
                                             command=self.aircraft_tree.yview)
        self.aircraft_scroll.grid(row=6, column=4, sticky='nsew')
        self.aircraft_tree.configure(yscrollcommand=self.aircraft_scroll.set)

    def view_aircraft(self):
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT aircraft_id, registration_number, aircraft_type, capacity, airline_id, airport_id FROM Aircrafts")
            rows = cursor.fetchall()
            self.aircraft_tree.delete(*self.aircraft_tree.get_children())
            for row in rows:
                self.aircraft_tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch aircraft: {e}")
        finally:
            conn.close()

    def add_airline(self):
        entries = [self.airline_name_entry, self.airline_country_entry, self.airline_website_entry]
        if not all(is_entry_valid(entry) for entry in entries):
            messagebox.showerror("Error", "All fields must be filled out.")
            return
        airline_name =self.airline_name_entry.get()
        country = self.airline_country_entry.get()
        website = self.airline_website_entry.get()
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""INSERT INTO Airlines (airline_name, country, website)
                              VALUES (%s, %s, %s)""",
                           (airline_name, country, website))
            conn.commit()
            messagebox.showinfo("Success", "Airline added successfully")
        except Exception as e:
            messagebox.showerror("Error", "Failed to add airline")
            print(e)
        finally:
            conn.close()
        self.view_airlines()  # Automatically update the view after adding

    def setup_aircrafts_tab(self):
        self.aircrafts_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.aircrafts_tab, text='Aircrafts')

        # Labels and Entries for aircraft details
        ttk.Label(self.aircrafts_tab, text='Registration Number:').grid(row=0, column=0, padx=10, pady=10)
        self.registration_number_entry = ttk.Entry(self.aircrafts_tab)
        self.registration_number_entry.grid(row=0, column=1,sticky= "nsew")

        ttk.Label(self.aircrafts_tab, text='Aircraft Type:').grid(row=1, column=0)
        self.aircraft_type_entry = ttk.Entry(self.aircrafts_tab)
        self.aircraft_type_entry.grid(row=1, column=1,sticky= "nsew")

        ttk.Label(self.aircrafts_tab, text='Capacity:').grid(row=2, column=0)
        self.capacity_entry = ttk.Entry(self.aircrafts_tab)
        self.capacity_entry.grid(row=2, column=1,sticky= "nsew")

        ttk.Label(self.aircrafts_tab, text='Airline ID:').grid(row=3, column=0)
        self.airline_id_entry = ttk.Entry(self.aircrafts_tab)
        self.airline_id_entry.grid(row=3, column=1,sticky= "nsew")

        ttk.Label(self.aircrafts_tab, text='Airport ID:').grid(row=4, column=0)
        self.airport_id_entry = ttk.Entry(self.aircrafts_tab)
        self.airport_id_entry.grid(row=4, column=1,sticky= "nsew")

        # Buttons for managing aircraft
        ttk.Button(self.aircrafts_tab, text='Add Aircraft', command=self.add_aircraft).grid(row=5, column=0,
                                                                                            sticky=tk.W, pady=10)
        ttk.Button(self.aircrafts_tab, text='View Aircraft', command=self.view_aircraft).grid(row=5, column=1,
                                                                                              sticky=tk.W)
        ttk.Button(self.aircrafts_tab, text='Delete Aircraft', command=self.delete_selected_aircraft).grid(row=5,
                                                                                                           column=2,
                                                                                                           sticky=tk.W,
                                                                                                           pady=10)

        # Treeview for displaying aircraft
        self.aircraft_tree = ttk.Treeview(self.aircrafts_tab, columns=(
            "Aircraft ID", "Registration Number", "Aircraft Type", "Capacity", "Airline ID", "Airport ID"),
                                          show="headings")
        self.aircraft_tree.grid(row=6, column=0, columnspan=4, pady=10, padx=10)
        for col in self.aircraft_tree["columns"]:
            self.aircraft_tree.heading(col, text=col)
            self.aircraft_tree.column(col, anchor=tk.CENTER)
            self.aircraft_tree.column(col, width=150)  # Adjust the width as needed

        # Scrollbar for the Treeview
        self.aircraft_scroll = ttk.Scrollbar(self.aircrafts_tab, orient="vertical",
                                             command=self.aircraft_tree.yview)
        self.aircraft_scroll.grid(row=6, column=4, sticky='ns')
        self.aircraft_tree.configure(yscrollcommand=self.aircraft_scroll.set)

    def view_airlines(self):
        """Fetch and display airlines from the database."""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM AirlinesWithTotalFlights")
            cursor.execute("SELECT airline_id, airline_name, country, website FROM Airlines")
            rows = cursor.fetchall()
            self.airlines_tree.delete(*self.airlines_tree.get_children())
            for row in rows:
                self.airlines_tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", "Failed to fetch airlines")
            print(e)
        finally:
            conn.close()

    def add_crew_member(self):
        entries = [self.registration_number_entry, self.aircraft_type_entry, self.capacity_entry, self.airline_id_entry,
                   self.airport_id_entry]
        if not all(is_entry_valid(entry) for entry in entries):
            messagebox.showerror("Error", "All fields must be filled out.")
            return
        """Insert a new crew member into the database."""
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        position = self.position_entry.get()
        experience = self.experience_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""INSERT INTO Crew_Members (first_name, last_name, position, experience)
                              VALUES (%s, %s, %s, %s)""",
                           (first_name, last_name, position, experience))
            conn.commit()
            messagebox.showinfo("Success", "Crew member added successfully")
        except Exception as e:
            messagebox.showerror("Error", "Failed to add crew member")
            print(e)
        finally:
            conn.close()
        self.view_crew()  # Automatically update the view after adding

    def view_crew(self):
        """Fetch and display crew members from the database."""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT crew_id, first_name, last_name, position, experience FROM Crew_Members")
            rows = cursor.fetchall()
            self.crew_tree.delete(*self.crew_tree.get_children())
            for row in rows:
                self.crew_tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch crew members: {e}")
        finally:
            conn.close()

    def setup_passengers_tab(self):
        self.passengers_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.passengers_tab, text='Passengers')

        # Labels and Entries for passenger details
        ttk.Label(self.passengers_tab, text='First Name:').grid(row=0, column=0, padx=10, pady=5)
        self.first_name_entry = ttk.Entry(self.passengers_tab)
        self.first_name_entry.grid(row=0, column=1, sticky= "nsew")

        ttk.Label(self.passengers_tab, text='Last Name:').grid(row=1, column=0, padx=10, pady=5)
        self.last_name_entry = ttk.Entry(self.passengers_tab)
        self.last_name_entry.grid(row=1, column=1, sticky="nsew")

        ttk.Label(self.passengers_tab, text='Phone Number:').grid(row=2, column=0, padx=10, pady=5)
        self.phone_number_entry = ttk.Entry(self.passengers_tab)
        self.phone_number_entry.grid(row=2, column=1, sticky="nsew")

        ttk.Label(self.passengers_tab, text='Email:').grid(row=3, column=0, padx=10, pady=5)
        self.email_entry = ttk.Entry(self.passengers_tab)
        self.email_entry.grid(row=3, column=1, sticky="nsew")

        # Buttons for managing passengers
        ttk.Button(self.passengers_tab, text='Add Passenger', command=self.add_passenger, width=5).grid(row=4, column=0, pady=10,
                                                                                               sticky="ew")
        ttk.Button(self.passengers_tab, text='View Passengers', command=self.view_passengers, width = 5).grid(row=4, column=1,
                                                                                                   pady=10, sticky="ew")
        ttk.Button(self.passengers_tab, text='Delete Passenger', command=self.delete_selected_passenger, width= 5).grid(row=4,
                                                                                                              column=2,
                                                                                                              pady=10,
                                                                                                              sticky="ew")

        # Treeview for displaying passengers
        self.passengers_tree = ttk.Treeview(self.passengers_tab, columns=(
        "Passenger ID", "First Name", "Last Name", "Phone Number", "Email"), show="headings")
        self.passengers_tree.grid(row=5, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
        for col in self.passengers_tree["columns"]:
            self.passengers_tree.heading(col, text=col)
            self.passengers_tree.column(col, anchor=tk.CENTER)
            self.passengers_tree.column(col, width=150)  # Adjust the width as needed

        # Scrollbar for the Treeview
        self.passenger_scroll = ttk.Scrollbar(self.passengers_tab, orient="vertical",
                                              command=self.passengers_tree.yview)
        self.passenger_scroll.grid(row=5, column=3, sticky='ns')
        self.passengers_tree.configure(yscrollcommand=self.passenger_scroll.set)

    def add_passenger(self):
        entries = [self.first_name_entry, self.last_name_entry, self.phone_number_entry, self.email_entry]
        if not all(is_entry_valid(entry) for entry in entries):
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        phone_number = self.phone_number_entry.get().strip()
        email = self.email_entry.get().strip()

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""INSERT INTO Passengers (first_name, last_name, phone_number, email)
                              VALUES (%s, %s, %s, %s)""",
                           (first_name, last_name, phone_number, email))
            conn.commit()
            messagebox.showinfo("Success", "Passenger added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add passenger: {e}")
        finally:
            conn.close()
        self.view_passengers()

    def view_passengers(self):
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT passenger_id, first_name, last_name, phone_number, email FROM Passengers")
            rows = cursor.fetchall()
            self.passengers_tree.delete(*self.passengers_tree.get_children())
            for row in rows:
                self.passengers_tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch passengers: {e}")
        finally:
            conn.close()

    def delete_selected_airline(self):
        selected_item = self.airlines_tree.selection()
        if selected_item:
            airline_id = self.airlines_tree.item(selected_item, "values")[0]  # Assuming ID is in the first column
            if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this airline?"):
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Airlines WHERE airline_id=?", (airline_id,))
                conn.commit()
                conn.close()
                self.view_airlines()
        else:
            messagebox.showerror("Error", "Please select an airline to delete.")

    def delete_selected_aircraft(self):
        selected_item = self.aircraft_tree.selection()
        if selected_item:
            aircraft_id = self.aircraft_tree.item(selected_item, "values")[0]
            if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this aircraft?"):
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Aircrafts WHERE aircraft_id=%s", (aircraft_id,))
                conn.commit()
                conn.close()
                self.view_aircraft()
        else:
            messagebox.showerror("Error", "Please select an aircraft to delete.")

    def delete_selected_crew_member(self):
        selected_item = self.crew_tree.selection()
        if selected_item:
            crew_id = self.crew_tree.item(selected_item, "values")[0]
            if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this crew member?"):
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Crew_Members WHERE crew_id=%s", (crew_id,))
                conn.commit()
                conn.close()
                self.view_crew()
        else:
            messagebox.showerror("Error", "Please select a crew member to delete.")

    def delete_selected_passenger(self):
        selected_item = self.passengers_tree.selection()
        if selected_item:
            passenger_id = self.passengers_tree.item(selected_item, "values")[0]
            if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this passenger?"):
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Passengers WHERE passenger_id=%s", (passenger_id,))
                conn.commit()
                conn.close()
                self.view_passengers()
        else:
            messagebox.showerror("Error", "Please select a passenger to delete.")

    def delete_selected_booking(self):
        selected_item = self.bookings_tree.selection()
        if selected_item:
            booking_id = self.bookings_tree.item(selected_item, "values")[0]
            if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this booking?"):
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Bookings WHERE booking_id=%s", (booking_id,))
                conn.commit()
                conn.close()
                self.refresh_bookings()
        else:
            messagebox.showerror("Error", "Please select a booking to delete.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AirlineApp(root)
    root.mainloop()
