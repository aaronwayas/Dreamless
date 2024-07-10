import flet as ft
import utils.mclib as mclib

import webbrowser
import os
import json
import time


def close_dialog(page: ft.Page):
    page.dialog.open = False
    page.update()


def get_versions():
    try:
        versions_installed = mclib.get_installed_versions(
            mclib.minecraft_directory,
        )
        all_versions = mclib.get_all_versions()
    except Exception as e:
        raise Exception("Error retrieving versions: " + str(e))

    all_vanilla_versions_except = [
        version["id"]
        for version in all_versions
        if version["type"] == "release" and version["id"] not in versions_installed
    ]

    all_vanilla_versions = [
        version["id"] for version in all_versions if version["type"] == "release"
    ]

    return versions_installed, all_vanilla_versions_except, all_vanilla_versions


def download_vanilla(page: ft.Page):
    print("Download Vanilla")

    def on_set_status(text):
        status_label.value = text
        page.update()

    version = version_to_download.value
    print(f"Version to download: {version}")

    status_label.visible = True
    progress_bar_download.visible = True
    page.update()

    callback = {"setStatus": on_set_status}
    success = mclib.download_version(version, callback)

    if success:
        print(f"Download Version Complete: {version} in {mclib.minecraft_directory}")
        progress_bar_download.value = 1
        page.dialog = create_alert_dialog(
            page, "Success", "Download complete.", lambda _: close_dialog(page)
        )
        page.dialog.open = True
    else:
        print("Download failed.")
        page.dialog = create_alert_dialog(
            page, "Error", "Download failed.", lambda _: close_dialog(page)
        )
        page.dialog.open = True

    page.update()


def download_forge(page: ft.Page):
    print("Download Forge")

    def on_set_status(text):
        status_label.value = text
        page.update()

    version = forge_version.value
    print(f"Version to download: {version}")

    status_label.visible = True
    progress_bar_download.visible = True
    page.update()

    callback = {"setStatus": on_set_status}
    success = mclib.download_forge_version(version, callback)

    if success:
        print(f"Download Version Complete: {version} in {mclib.minecraft_directory}")
        page.dialog = create_alert_dialog(
            page, "Success", "Download complete.", lambda _: close_dialog(page)
        )
        page.dialog.open = True
    else:
        print("Download failed.")
        page.dialog = create_alert_dialog(
            page, "Error", "Download failed.", lambda _: close_dialog(page)
        )

    page.update()


def search_forge_version(page: ft.Page, e):
    version = mclib.get_forge_version(e.control.value)
    forge_version.value = version
    forge_version.options = [ft.dropdown.Option(version)]
    download_button.on_click = lambda e: download_forge(page)
    page.update()


def select_version(page: ft.Page, e):
    status_label.visible = False
    progress_bar_download.visible = False

    if e.control.value == "Vanilla":
        version_to_download.options = [
            ft.dropdown.Option(version) for version in get_versions()[1]
        ]
        version_to_download.value = get_versions()[1][0]
        version_to_download.label = "Version"
        version_to_download.on_change = None
    elif e.control.value == "Forge":
        version_to_download.options = [
            ft.dropdown.Option(version) for version in get_versions()[2]
        ]
        version_to_download.value = get_versions()[2][0]
        version_to_download.label = "Vanilla Version"
        forge_version.visible = True
        version_to_download.on_change = lambda e: search_forge_version(page, e)

    page.update()


def create_alert_dialog(page, title: str, content: str, action):
    return ft.AlertDialog(
        modal=True,
        title=ft.Text(title),
        content=ft.Text(content),
        actions=[
            ft.TextButton(
                content=ft.Text("OK", color="white"),
                on_click=action,
                style=ft.ButtonStyle(bgcolor="#801AE5"),
            )
        ],
    )


def run_minecraft(page: ft.Page, e) -> None:
    username, ram = mclib.get_config("utils/config.json")
    version = dropdown_version.value

    if not username or not ram:
        page.dialog = create_alert_dialog(
            page,
            "Error",
            "Please enter a username and RAM.",
            lambda _: close_dialog(page),
        )
        page.dialog.open = True
        page.update()
        return

    e.control.disabled = True
    page.update()

    try:
        print(f"Run Minecraft: {username}, {ram} GB, {version}\n")
        mclib.run_minecraft(username, ram, version)

    except Exception as e:
        page.dialog = create_alert_dialog(
            page, "Error", f"Error running Minecraft: {e}", lambda _: close_dialog(page)
        )

        page.dialog.open = True
        page.update()
        return

    time.sleep(1)
    e.control.disabled = False
    page.update()


def save_config(page: ft.Page):
    username = text_field_username.value
    ram = dropdown_ram.value

    if not username or not ram:
        page.dialog = create_alert_dialog(
            page,
            "Error",
            "Please enter a username and RAM.",
            lambda _: close_dialog(page),
        )

        page.dialog.open = True
        page.update()
        return

    print(f"Save Config: {username}, {ram}")
    mclib.write_config("utils/config.json", username, ram)

    page.dialog = create_alert_dialog(
        page, "Success", "Config saved successfully.", lambda _: close_dialog(page)
    )

    page.dialog.open = True
    page.update()


def bar_menu(page: ft.Page) -> ft.Container:
    container_1 = ft.Container(
        content=ft.Row(
            [
                ft.TextButton(
                    content=ft.Text("Download", color="black", size=20),
                    on_click=lambda _: page.go("/download"),
                ),
                ft.TextButton(
                    content=ft.Text("Settings", color="black", size=20),
                    on_click=lambda _: page.go("/settings"),
                ),
                ft.FilledButton(
                    content=ft.Text(
                        "Feedback", color="white", size=14, weight=ft.FontWeight.BOLD
                    ),
                    style=ft.ButtonStyle(
                        bgcolor="#801AE5", shape=ft.RoundedRectangleBorder(radius=12)
                    ),
                    on_click=lambda _: webbrowser.open(
                        "https://github.com/aaronwayas/Dreamless"
                    ),
                ),
                ft.FilledButton(
                    content=ft.Text(
                        "Help", color="white", size=14, weight=ft.FontWeight.BOLD
                    ),
                    style=ft.ButtonStyle(
                        bgcolor="#801AE5", shape=ft.RoundedRectangleBorder(radius=20)
                    ),
                    on_click=lambda _: webbrowser.open("https://discord.gg/tarfQNevpf"),
                ),
            ],
            alignment=ft.MainAxisAlignment.END,
        ),
    )

    container = ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.TextButton(
                        content=ft.Text(
                            "Dreamless",
                            color="black",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                        ),
                        on_click=lambda _: page.go("/"),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10)
                        ),
                    ),
                ),
                container_1,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        alignment=ft.alignment.center_right,
    )
    return container


def main(page: ft.Page):
    global dropdown_version, dropdown_ram, text_field_username, version_to_download, progress_bar_download, status_label, forge_version, download_button, type_version

    page.title = "Dreamless"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.min_height = page.height / 2
    page.window.min_width = page.width / 2

    download_button = ft.FilledButton(
        content=ft.Text("Download", size=16, weight=ft.FontWeight.BOLD),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=20), bgcolor="#801AE5"
        ),
        height=40,
        width=600,
        on_click=lambda e: download_vanilla(page),
    )

    dropdown_version = ft.Dropdown(
        options=[ft.dropdown.Option(version) for version in get_versions()[0]],
        value=get_versions()[0][0],
        on_change=lambda e: print(e.control.value),
        border_radius=ft.border_radius.all(12),
        content_padding=ft.padding.only(left=10),
        border_width=1,
        border_color="#D9C7EB",
        focused_color="#703BA6",
        label_style=ft.TextStyle(color="#703BA6"),
    )

    dropdown_ram = ft.Dropdown(
        label="RAM",
        options=[
            ft.dropdown.Option("2"),
            ft.dropdown.Option("4"),
            ft.dropdown.Option("8"),
            ft.dropdown.Option("16"),
        ],
        value=mclib.get_config("utils/config.json")[1],
        border_width=1,
        border_color="#D9C7EB",
        border_radius=ft.border_radius.all(12),
        focused_color="#703BA6",
        label_style=ft.TextStyle(color="#703BA6"),
        suffix_text="GB",
        suffix_style=ft.TextStyle(color="#703BA6"),
    )

    text_field_username = ft.TextField(
        label="Username",
        value=mclib.get_config("utils/config.json")[0],
        border_width=1,
        border_color="#D9C7EB",
        border_radius=ft.border_radius.all(12),
        focused_color="#703BA6",
        label_style=ft.TextStyle(color="#703BA6"),
    )

    version_to_download = ft.Dropdown(
        label="Version",
        border_width=1,
        border_color="#D9C7EB",
        border_radius=ft.border_radius.all(12),
        focused_color="#703BA6",
        label_style=ft.TextStyle(color="#703BA6"),
        expand=True,
    )

    progress_bar_download = ft.ProgressBar(
        visible=False,
        color="#801AE5",
    )

    status_label = ft.Text("Progress", size=14, visible=False)

    forge_version = ft.Dropdown(
        label="Forge Version",
        border_width=1,
        border_color="#D9C7EB",
        border_radius=ft.border_radius.all(12),
        focused_color="#703BA6",
        label_style=ft.TextStyle(color="#703BA6"),
        expand=True,
    )

    forge_version.disabled = False
    forge_version.visible = False

    type_version = ft.Dropdown(
        label="Type of Minecraft",
        options=[ft.dropdown.Option("Vanilla"), ft.dropdown.Option("Forge")],
        on_change=lambda _: select_version(page, _),
        border_width=1,
        border_color="#D9C7EB",
        border_radius=ft.border_radius.all(12),
        focused_color="#703BA6",
        label_style=ft.TextStyle(color="#703BA6"),
    )

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    def route_change(route):
        if page.route != route:
            page.views.clear()
            page.views.append(
                ft.View(
                    "/",
                    [
                        bar_menu(page),
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Container(
                                            content=ft.Image(
                                                src="assets/image_1.png",
                                                fit=ft.ImageFit.FIT_HEIGHT,
                                            ),
                                        ),
                                        padding=ft.padding.only(
                                            right=20, bottom=20, top=20
                                        ),
                                        expand=True,
                                    ),
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Text(
                                                    "Version", weight=ft.FontWeight.BOLD
                                                ),
                                                dropdown_version,
                                                ft.Container(
                                                    ft.FilledButton(
                                                        content=ft.Text(
                                                            "Play",
                                                            color="white",
                                                            size=16,
                                                            weight=ft.FontWeight.BOLD,
                                                        ),
                                                        style=ft.ButtonStyle(
                                                            bgcolor="#801AE5",
                                                            shape=ft.RoundedRectangleBorder(
                                                                radius=20
                                                            ),
                                                        ),
                                                        width=1000,
                                                        on_click=lambda e: run_minecraft(
                                                            page, e
                                                        ),
                                                    ),
                                                    alignment=ft.alignment.top_left,
                                                ),
                                                ft.Container(
                                                    content=ft.TextButton(
                                                        text="Buy Minecraft",
                                                        icon=ft.icons.OPEN_IN_NEW,
                                                        icon_color="black",
                                                        on_click=lambda e: webbrowser.open(
                                                            "https://www.minecraft.net/es-es/store/minecraft-java-bedrock-edition-pc"
                                                        ),
                                                        style=ft.ButtonStyle(
                                                            shape=ft.RoundedRectangleBorder(
                                                                radius=20
                                                            ),
                                                        ),
                                                    ),
                                                    alignment=ft.alignment.top_left,
                                                ),
                                            ],
                                        ),
                                        expand=True,
                                        padding=ft.padding.only(
                                            top=30, left=5, right=5
                                        ),
                                    ),
                                ],
                            ),
                            expand=True,
                        ),
                    ],
                ),
            )

        if page.route == "":
            page.go("/")
            page.title = "Dreamless"

        elif page.route == "/settings":
            if not os.path.exists("utils/config.json"):
                with open("utils/config.json", "w") as f:
                    json.dump({"username": "", "ram": ""}, f)

            page.views.append(
                ft.View(
                    "/settings",
                    [
                        bar_menu(page),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Settings", size=20),
                                    text_field_username,
                                    dropdown_ram,
                                ]
                            ),
                            expand=True,
                            padding=ft.padding.only(left=10, right=10),
                        ),
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.FilledButton(
                                        content=ft.Text(
                                            "Save", size=16, weight=ft.FontWeight.BOLD
                                        ),
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=20),
                                            bgcolor="#801AE5",
                                        ),
                                        height=40,
                                        width=170,
                                        on_click=lambda e: save_config(page),
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ),
                    ],
                )
            )

            page.title = "Dreamless - Settings"

        elif page.route == "/download":
            page.views.append(
                ft.View(
                    "/download",
                    [
                        bar_menu(page),
                        ft.Container(
                            content=ft.Text("Download", size=20),
                            alignment=ft.alignment.center_left,
                            height=40,
                            padding=ft.padding.only(left=10),
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    type_version,
                                    ft.Container(
                                        content=ft.Row(
                                            controls=[
                                                version_to_download,
                                                forge_version,
                                            ],
                                            expand=True,
                                        ),
                                    ),
                                    status_label,
                                    progress_bar_download,
                                    download_button,
                                ],
                            ),
                            expand=True,
                            padding=ft.padding.only(left=10, right=10),
                        ),
                    ],
                )
            )
            page.title = "Dreamless - Download"

        elif page.route == "/":
            page.title = "Dreamless"

        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main, view=ft.FLET_APP, assets_dir="assets")
