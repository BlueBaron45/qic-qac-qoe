import datetime
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, DataTable, Footer, Header, Static

# --- Custom Widget: Stat Box ---
class StatCard(Static):
    """A card widget to display a single metric."""
    def __init__(self, title: str, value: str, **kwargs):
        super().__init__(**kwargs)
        self.title_text = title
        self.value_text = value

    def compose(self) -> ComposeResult:
        yield Static(self.title_text, classes="stat-title")
        yield Static(self.value_text, classes="stat-value")


# --- Main Dashboard Application ---
class DashboardApp(App):
    """A Textual Dashboard Application."""

    # Built-in CSS for layout and design styling
    CSS = """
    Screen {
        layout: vertical;
        background: $surface;
    }

    #body {
        height: 1fr;
    }

    #sidebar {
        width: 26;
        background: $panel;
        padding: 1;
        border-right: heavy $accent;
    }

    #content {
        padding: 1;
    }

    .stats-row {
        height: 8;
        margin-bottom: 1;
    }

    StatCard {
        background: $boost;
        border: solid $accent;
        padding: 1;
        margin-right: 1;
        width: 1fr;
    }

    .stat-title {
        color: $text-muted;
        text-style: bold;
    }

    .stat-value {
        color: $success;
        text-style: bold;
        padding-top: 1;
    }

    DataTable {
        height: 1fr;
        border: solid $primary;
    }

    Button {
        width: 100%;
        margin-top: 1;
    }
    """

    # Keyboard shortcut bindings shown in the Footer
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh_data", "Refresh Data"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Horizontal(id="body"):
            # Sidebar Navigation / Actions
            with Vertical(id="sidebar"):
                yield Static("### Dashboard Menu", classes="sidebar-title")
                yield Button("Refresh Metrics", id="btn-refresh", variant="primary")
                yield Button("Clear Table", id="btn-clear", variant="warning")
                yield Button("Quit App", id="btn-quit", variant="error")

            # Main Dashboard Panel
            with Vertical(id="content"):
                # Top Row: Stat Cards
                with Horizontal(classes="stats-row"):
                    yield StatCard("ACTIVE USERS", "1,284", id="card-users")
                    yield StatCard("CPU LOAD", "42.5%", id="card-cpu")
                    yield StatCard("SERVER STATUS", "ONLINE", id="card-status")

                # Bottom Area: Interactive Data Table
                yield DataTable(id="data-table")

        yield Footer()

    def on_mount(self) -> None:
        """Runs automatically when the app loads."""
        table = self.query_one("#data-table", DataTable)
        table.add_columns("Timestamp", "Service Name", "Status", "Latency (ms)")
        
        # Populate initial dummy data
        self.populate_table()

    def populate_table(self) -> None:
        table = self.query_one("#data-table", DataTable)
        table.clear()
        
        now = datetime.datetime.now().strftime("%H:%M:%S")
        records = [
            (now, "Authentication API", "OK", "24ms"),
            (now, "Database Cluster", "OK", "4ms"),
            (now, "Payment Gateway", "WARN", "180ms"),
            (now, "Notification Service", "OK", "45ms"),
            (now, "Storage Bucket", "OK", "12ms"),
        ]
        
        for record in records:
            table.add_row(*record)

    # Event Handlers for Buttons
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-refresh":
            self.action_refresh_data()
        elif event.button.id == "btn-clear":
            self.query_one("#data-table", DataTable).clear()
        elif event.button.id == "btn-quit":
            self.exit()

    # Custom action bound to keyboard 'r' or refresh button
    def action_refresh_data(self) -> None:
        self.populate_table()
        self.notify("Dashboard metrics updated!")


if __name__ == "__main__":
    app = DashboardApp()
    app.run()