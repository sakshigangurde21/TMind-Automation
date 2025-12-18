import unittest
from Asset import AssetsTests  # Import the test class from your Asset.py
from Device import DevicesTests
from ManageUser import ManageUserTests
from Signals import SignalTests
from Tour import TourTests


def suite():
    suite = unittest.TestSuite()
    
    # ---------------- RUN SPECIFIC ASSET TESTS ----------------
    # Basic page open
    # suite.addTest(AssetsTests('test_open_assets_page'))
    
    # # Create root asset
    # suite.addTest(AssetsTests('test_create_root_asset'))
    
    # suite.addTest(AssetsTests('test_search_asset'))
    # suite.addTest(AssetsTests('test_search_partial_match'))
    # # Add child asset
    # suite.addTest(AssetsTests('test_add_child_asset'))
    
    # # Edit asset
    # suite.addTest(AssetsTests('test_edit_asset'))
    # suite.addTest(AssetsTests('test_no_asset_selected_shows_empty_details'))
    
    # # Asset details verification
    # suite.addTest(AssetsTests('test_asset_details_visible'))
    
    # # Delete child asset
    # suite.addTest(AssetsTests('test_delete_child_asset'))
    # # Delete parent asset
    # suite.addTest(AssetsTests('test_delete_parent_asset'))
    # suite.addTest(AssetsTests('test_duplicate_asset_name'))
    # suite.addTest(AssetsTests('test_empty_asset_name_not_allowed'))
    # suite.addTest(AssetsTests('test_asset_invalid_characters'))
    # suite.addTest(AssetsTests('test_asset_name_too_long'))
    # suite.addTest(AssetsTests('test_delete_icon_rules'))
    # suite.addTest(AssetsTests('test_asset_hierarchy_depth_limit'))


    # ---------------- DEVICES TESTS ----------------
    # suite.addTest(DevicesTests('test_navigate_to_device_module'))
    # suite.addTest(DevicesTests('test_add_device_success'))
    # suite.addTest(DevicesTests('test_add_device_empty_name'))
    # suite.addTest(DevicesTests('test_add_device_empty_description_allowed'))
    # suite.addTest(DevicesTests('test_device_name_special_car123'))
    # suite.addTest(DevicesTests('test_device_name_special_symbols'))
    # suite.addTest(DevicesTests('test_device_name_special_dash'))
    # suite.addTest(DevicesTests('test_device_name_too_short'))
    # suite.addTest(DevicesTests('test_device_name_too_long'))
    # suite.addTest(DevicesTests('test_add_duplicate_device_name'))
    # suite.addTest(DevicesTests('test_delete_device'))
    # suite.addTest(DevicesTests('test_delete_device_cancel'))
    # suite.addTest(DevicesTests('test_edit_device_name_success'))
    # suite.addTest(DevicesTests('test_edit_device_without_name'))
    # suite.addTest(DevicesTests('test_search_device'))
    # suite.addTest(DevicesTests('test_search_non_existing_device'))
    # suite.addTest(DevicesTests('test_open_device_config_page'))
    # suite.addTest(DevicesTests('test_save_device_configuration'))
    # # Poll Interval
    # suite.addTest(DevicesTests('test_edit_poll_interval_below_min'))
    # suite.addTest(DevicesTests('test_edit_poll_interval_above_max'))
    # suite.addTest(DevicesTests('test_edit_poll_interval_empty'))

    # # IP Address
    # suite.addTest(DevicesTests('test_edit_ip_random_text'))
    # suite.addTest(DevicesTests('test_edit_ip_wrong_format'))
    # suite.addTest(DevicesTests('test_edit_ip_letters_only'))
    # suite.addTest(DevicesTests('test_edit_ip_empty'))

    # # Port
    # suite.addTest(DevicesTests('test_edit_port_zero'))
    # suite.addTest(DevicesTests('test_edit_port_above_limit'))

    # ---------------- SLAVE MANAGER ----------------
    # suite.addTest(DevicesTests('test_open_slave_manager'))
    # suite.addTest(DevicesTests('test_open_new_slave_page'))
    # suite.addTest(DevicesTests('test_save_slave_without_register'))
    # suite.addTest(DevicesTests('test_open_add_register_popup'))
    # suite.addTest(DevicesTests('test_close_add_register_popup'))
    # suite.addTest(DevicesTests('test_add_register_success'))
    # suite.addTest(DevicesTests('test_cancel_register_popup'))
    # suite.addTest(DevicesTests('test_save_slave_after_register_add'))


    # suite.addTest(ManageUserTests('test_open_manage_user_page'))
    # suite.addTest(ManageUserTests('test_search_existing_user'))
    # suite.addTest(ManageUserTests('test_search_non_existing_user'))
    # suite.addTest(ManageUserTests('test_change_user_role'))
    # suite.addTest(ManageUserTests('test_delete_user_cancel'))
    # suite.addTest(ManageUserTests('test_delete_user_confirm'))
    # suite.addTest(ManageUserTests('test_download_csv'))
    # suite.addTest(ManageUserTests('test_download_csv_verification'))
    # suite.addTest(ManageUserTests('test_pagination_next_previous'))
    # suite.addTest(ManageUserTests('test_go_to_specific_page'))
    # suite.addTest(ManageUserTests('test_pagination_buttons_disabled_on_first_last_page'))
    # suite.addTest(ManageUserTests('test_search_filters_by_username_only'))
    # suite.addTest(ManageUserTests('test_csv_download_shows_toast'))


    # suite.addTest(SignalTests('test_open_signal_page'))
    # # ---------------- MAIN ASSET ----------------
    # suite.addTest(SignalTests('test_select_main_asset'))

    # # ---------------- ASSIGNED DEVICE ----------------
    # suite.addTest(SignalTests('test_asset_without_device_shows_not_assigned'))

    # # ---------------- SIGNAL VISIBILITY ----------------
    # suite.addTest(SignalTests('test_no_device_no_signals'))

    # # ---------------- GRAPH ----------------
    # suite.addTest(SignalTests('test_graph_empty_state'))
    # suite.addTest(SignalTests('test_graph_visible_for_asset_with_signals'))

    # # ---------------- COMPARE ASSET ----------------
    # suite.addTest(SignalTests('test_select_compare_asset'))

    # # ---------------- DATA CONSISTENCY ----------------
    # suite.addTest(SignalTests('test_device_signal_consistency'))
    # suite.addTest(SignalTests('test_signals_change_when_asset_changes'))



    # ---------------- TOUR TESTS ----------------
    suite.addTest(TourTests('test_start_tour_button_visible'))
    suite.addTest(TourTests('test_start_tour'))
    suite.addTest(TourTests('test_next_prev_buttons'))
    suite.addTest(TourTests('test_close_tour'))
    suite.addTest(TourTests('test_complete_tour'))
    suite.addTest(TourTests('test_popover_title_description_not_empty'))


    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
