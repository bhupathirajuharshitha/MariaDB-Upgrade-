import mariadb
import sys
import getpass
import subprocess

def print_section_header(title):
    print("\n" + "=" * 60)
    print(f"{title:^60}")
    print("=" * 60)

def print_option_details(option, old_default, new_default, description):
    print(f"\n> Option: {option}")
    print(f"  - Old Default: {old_default}")
    print(f"  - New Default: {new_default}")
    print(f"  - Description: {description}")

def connect_to_mariadb(hostname, username, password):
    try:
        conn = mariadb.connect(
            host=hostname,
            user=username,
            password=password
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def get_mariadb_version(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()[0]
    return version

def upgrade_dependencies_10_4_to_10_5(hostname, username, password):
    print_section_header("Upgrading Dependencies 10.4 to 10.5")
    
    options = [
        "innodb_adaptive_hash_index", "innodb_checksum_algorithm",
        "innodb_log_optimize_ddl", "slave_parallel_mode",
        "performance_schema_max_cond_classes", "performance_schema_max_file_classes",
        "performance_schema_max_mutex_classes", "performance_schema_max_rwlock_classes",
        "performance_schema_setup_actors_size", "performance_schema_setup_objects_size"
    ]

    new_defaults = ["OFF", "full_crc32", "OFF", "optimistic", "90", "80", "210", "50", "-1", "-1"]
    old_defaults = ["ON","crc32","ON","conservative","80","50","200","40","100","100"]
    descriptions = [
        "Controls the use of the adaptive hash index, reducing potential overhead.",
        "Switches to a more comprehensive checksum algorithm.",
        "Disables optimization in the logging of DDL statements.",
        "Changes parallel slave execution mode to a more aggressive approach.",
        "Increases the number of condition classes available in the performance schema.",
        "Expands the number of file classes for performance monitoring.",
        "Boosts the count of mutex classes in performance data collection.",
        "Enhances the tracking of read-write lock classes in the performance schema.",
        "Sets the setup actors size to unlimited, if not explicitly defined.",
        "Defines setup objects size to unlimited, optimizing storage."
    ]

    for i, option in enumerate(options):
        print_option_details(option, old_defaults[i], new_defaults[i], descriptions[i])

    print("\nDeprecated Options:")
    deprecated_options = [
        "innodb_adaptive_max_sleep_delay", "innodb_background_scrub_data_check_interval",
        "innodb_background_scrub_data_interval", "innodb_background_scrub_data_compressed",
        "innodb_background_scrub_data_uncompressed", "innodb_buffer_pool_instances",
        "innodb_commit_concurrency", "innodb_concurrency_tickets",
        "innodb_log_files_in_group", "innodb_log_optimize_ddl",
        "innodb_page_cleaners", "innodb_replication_delay",
        "innodb_scrub_log", "innodb_scrub_log_speed",
        "innodb_thread_concurrency", "innodb_thread_sleep_delay",
        "innodb_undo_logs", "large_page_size"
    ]
    for option in deprecated_options:
        print(f"  - {option}")

def upgrade_dependencies_10_5_to_10_6(hostname, username, password):
    print_section_header("Upgrading Dependencies 10.5 to 10.6")

    print("\nChecking for usage of the reserved word 'OFFSET' in names...")
    try:
        conn = mariadb.connect(
            host=hostname,
            user=username,
            password=password
        )
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name LIKE '%offset%';")
        offset_usage = cursor.fetchall()
    except mariadb.Error as e:
        print(f"Error querying MariaDB Platform: {e}")
        offset_usage = []
    finally:
        if conn:
            conn.close()

    print("New reserved word: OFFSET. This can no longer be used as an identifier without being quoted.")
    if not offset_usage:
        print("\nNo tables found using 'OFFSET' in their names.")
    else:
        print("  Tables using 'OFFSET' in their names:", [row[0] for row in offset_usage])

    print("\nListing tables with COMPRESSED row format...")
    print("\nFrom MariaDB 10.6.0 until MariaDB 10.6.5, tables that are of the COMPRESSED row format are read-only by default. This was intended to be the first step towards removing write support and deprecating the feature.This plan has been scrapped, and from MariaDB 10.6.6, COMPRESSED tables are no longer read-only by default.From MariaDB 10.6.0 to MariaDB 10.6.5, set the innodb_read_only_compressed variable to OFF to make the tables writable.")
    try:
        conn = mariadb.connect(
            host=hostname,
            user=username,
            password=password
        )
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE row_format = 'COMPRESSED';")
        compressed_tables = cursor.fetchall()
    except mariadb.Error as e:
        print(f"Error querying MariaDB Platform: {e}")
        compressed_tables = []
    finally:
        if conn:
            conn.close()

    if not compressed_tables:
        print("\nNo tables found using COMPRESSED row format.")
    else:
        print("  COMPRESSED Tables:", [row[0] for row in compressed_tables])

    options = [
        "character_set_client", "character_set_connection", "character_set_results", "character_set_system",
        "innodb_flush_method", "old_mode"
    ]

    old_defaults = ["utf8", "utf8", "utf8", "utf8", "fsync", "Empty"]
    new_defaults = ["utf8mb3", "utf8mb3", "utf8mb3", "utf8mb3", "O_DIRECT", "UTF8_IS_UTF8MB3"]
    descriptions = [
        "Sets the client's character set to utf8mb3 by default.",
        "Changes the connection's character set to utf8mb3.",
        "Results are now utf8mb3 coded by default.",
        "System character set set to utf8mb3 for backward compatibility.",
        "Flush method switched to O_DIRECT for direct disk access.",
        "Defines default character set behavior for utf8 aliases."
    ]
    for i, option in enumerate(options):
        print_option_details(option, old_defaults[i], new_defaults[i], descriptions[i])

    print("\nRemoved or Renamed Options:")
    removed_renamed_options = [
        "innodb_checksum_algorithm: The *innodb and *none options have been removed.",
        "innodb_commit_concurrency", "innodb_concurrency_tickets", "innodb_file_format", "innodb_large_prefix"
    ]
    for option in removed_renamed_options:
        print(f"  - {option}")

    print("\nDeprecated Options:")
    deprecated_options = [
        "wsrep_replicate_myisam: Use wsrep_mode instead.",
        "wsrep_strict_ddl: Use wsrep_mode instead."
    ]
    for option in deprecated_options:
        print(f"  - {option}")

def upgrade_dependencies_10_6_to_10_11(hostname, username, password):
    print_section_header("Upgrading Dependencies 10.6 to 10.11")

    options = [
        "innodb_buffer_pool_chunk_size", "spider_auto_increment_mode", "spider_bgs_first_read", "spider_bgs_mode",
        "spider_bgs_second_read", "spider_bka_mode", "spider_bka_table_name_type", "spider_buffer_size", 
        "spider_bulk_size", "spider_bulk_update_mode", "spider_bulk_update_size", "spider_casual_read", 
        "spider_connect_timeout", "spider_crd_bg_mode", "spider_crd_interval", "spider_crd_mode", "spider_crd_sync", 
        "spider_crd_type", "spider_crd_weight", "spider_delete_all_rows_type", "spider_direct_dup_insert", 
        "spider_direct_order_limit", "spider_error_read_mode", "spider_error_write_mode", "spider_first_read", 
        "spider_init_sql_alloc_size", "spider_internal_limit", "spider_internal_offset", "spider_internal_optimize", 
        "spider_internal_optimize_local", "spider_load_crd_at_startup", "spider_load_sts_at_startup", 
        "spider_low_mem_read", "spider_max_order", "spider_multi_split_read", "spider_net_read_timeout", 
        "spider_net_write_timeout", "spider_quick_mode", "spider_quick_page_byte", "spider_quick_page_size", 
        "spider_read_only_mode", "spider_reset_sql_alloc", "spider_second_read", "spider_selupd_lock_mode", 
        "spider_semi_split_read", "spider_semi_split_read_limit", "spider_semi_table_lock_connection", 
        "spider_semi_table_lock"
    ]

    old_defaults = [
        "134217728", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1",
        "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1",
        "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1",
        "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "1"
    ]

    new_defaults = [
        "Autosized", "0", "2", "0", "100", "1", "1", "16000", "16000", "0", "16000", "0", "6", "2", "51", "1", "0", "2",
        "2", "1", "0", "9223372036854775807", "0", "0", "0", "1024", "9223372036854775807", "0", "0", "0", "1", "1",
        "1", "32767", "100", "600", "600", "3", "10485760", "1024", "0", "1", "0", "1", "2", "1", "1", "0"
    ]

    descriptions = [
        "Controls InnoDB buffer pool chunk size, now autosized for optimization.",
        "Sets behavior for auto-increment columns; ensuring reliability.",
        "Enhances batch reading strategy for Spider engine.",
        "Manages batch processing for Spider engine operations, improving speed.",
        "Configures secondary batch read for Spider, handling queries efficiently.",
        "Optimizes batch key access for indexing.",
        "Specifies table name processing in BKA for compatibility.",
        "Defines Spider buffer size, crucial for large data transfers.",
        "Adjusts bulk processing size for large payloads.",
        "Sets mode for bulk update operations, facilitating batch changes.",
        "Determines bulk update size, enhancing batch update efficiency.",
        "Optimizes casual read performance for Spider queries.",
        "Adjusts connection timeout under Spider engine, enhancing reliability.",
        "Configures bg mode for CRD operations, improving asynchronous tasks.",
        "Sets CRD interval for periodic updates.",
        "Establishes mode for CRD operations, optimizing consistency.",
        "Syncs CRD processes, ensuring data integrity.",
        "Specifies CRD type, enhancing data tasks.",
        "Weights CRD procedure execution, allowing prioritization.",
        "Defines row deletion types in Spider, optimizing space management.",
        "Manages direct duplicate insert handling, reducing collision errors.",
        "Limits direct ordering, enhancing result handling.",
        "Sets error handling for read operations, ensuring robustness.",
        "Defines error handling mode for writes, ensuring reliability.",
        "Configures initial single read setups under Spider.",
        "Specifies SQL allocation size during setup.",
        "Establishes internal operation limits in Spider.",
        "Adjusts internal offset strategies.",
        "Optimizes internal Spider behaviors for local execution.",
        "Helps local data handling optimization during queries.",
        "Ensures CRD data loads at startup for readiness.",
        "Ensures stateful data loads for Spider operations in startup.",
        "Improves Spider read memory efficiency.",
        "Sets max order processing volume for high-performance.",
        "Optimizes split reading in multi-node Spider setups.",
        "Determines network read timeout for reliability.",
        "Adjusts network write timeout for stability.",
        "Optimizes quick mode for rapid Spider data transfer.",
        "Defines byte size for quick page processing.",
        "Decides page size for Spider queries, optimizing storage.",
        "Configures Spider read-only mode, restricting writes.",
        "Resets SQL allocation, tailoring resource usage.",
        "Controls secondary read setups for Spider.",
        "Adjusts locking strategies, maintaining integrity.",
        "Optimizes semi-split reads, using resources efficiently.",
        "Defines limits for semi-split tasks.",
        "Manages lock connections for semi-table access.",
        "Adjusts locking strategies, promoting concurrency."
    ]

    for i, option in enumerate(options):
        print_option_details(option, old_defaults[i], new_defaults[i], descriptions[i])

    removed_renamed_options = [
        "innodb_log_write_ahead_size: On Linux and Windows, physical block size is detected and used.",
        "innodb_version: Redundant.",
        "wsrep_replicate_myisam: Use wsrep_mode instead."
    ]
    for option in removed_renamed_options:
        print(f"  - {option}")

    print("\nDeprecated Options:")
    deprecated_options = [
        "keep_files_on_create: MariaDB now deletes orphan files, making this setting unnecessary."
    ]
    for option in deprecated_options:
        print(f"  - {option}")

def main():
    print_section_header("MariaDB Upgrade Assistant")
    hostname = input("Enter hostname: ")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    target_version = input("Enter target version: ")

    conn = connect_to_mariadb(hostname, username, password)
    current_version = get_mariadb_version(conn)
    
    print("\n" + "-" * 60)
    print(f"Current MariaDB version: {current_version}")
    print("-" * 60 + "\n")
    
    if current_version.startswith("10.4") and target_version == "10.11":
        upgrade_dependencies_10_4_to_10_5(hostname, username, password)
        upgrade_dependencies_10_5_to_10_6(hostname, username, password)
        upgrade_dependencies_10_6_to_10_11(hostname, username, password)
    elif current_version.startswith("10.5") and target_version == "10.11":
        upgrade_dependencies_10_5_to_10_6(hostname, username, password)
        upgrade_dependencies_10_6_to_10_11(hostname, username, password)
    elif current_version.startswith("10.6") and target_version == "10.11":
        upgrade_dependencies_10_6_to_10_11(hostname, username, password)

    conn.close()

if __name__ == "__main__":
    main()
