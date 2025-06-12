import mariadb
import sys
import getpass
import subprocess

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
    print("Upgrading dependencies from 10.4 to 10.5")
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
        "Sets the setup actors size, if not explicitly defined, to unlimited.",
        "Defines setup objects size to unlimited, optimizing storage."
    ]

    for i, option in enumerate(options):
        print(f"Option: {option}")
        print(f"  Old Default: {old_defaults[i]}")
        print(f"  New Default: {new_defaults[i]}")
        print(f"  Description: {descriptions[i]}")

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

    print("Listing deprecated options:")
    for option in deprecated_options:
        print(option)

def upgrade_dependencies_10_5_to_10_6(hostname, username, password):
    print("Upgrading dependencies from 10.5 to 10.6")
    print("Checking for usage of the reserved word 'OFFSET' in names...")
    result = subprocess.run(f"mysql -h {hostname} -u {username} -p{password} -e 'SELECT table_name FROM information_schema.tables WHERE table_name LIKE \"%offset%\";'", shell=True, capture_output=True, text=True)
    offset_usage = result.stdout.strip().split("\n")[1:]
    if not offset_usage:
        print("No tables found using 'OFFSET' in their names.")
    else:
        print("Tables using 'OFFSET' in their names:", offset_usage)

    print("Listing tables with COMPRESSED row format...")
    result = subprocess.run(f"mysql -h {hostname} -u {username} -p{password} -e 'SELECT table_name FROM information_schema.tables WHERE row_format = \"COMPRESSED\";'", shell=True, capture_output=True, text=True)
    compressed_tables = result.stdout.strip().split("\n")[1:]
    if not compressed_tables:
        print("No tables found using COMPRESSED row format.")
    else:
        print("COMPRESSED Tables:", compressed_tables)

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
     print(f"Option: {option}")
     print(f"  Old Default: {old_defaults[i]}")
     print(f"  New Default: {new_defaults[i]}")
     print(f"  Description: {descriptions[i]}")

    print("Listing options that have been removed or renamed:")
    removed_renamed_options = [
        "innodb_checksum_algorithm: The variable is still present, but the *innodb and *none options have been removed.",
        "innodb_commit_concurrency", "innodb_concurrency_tickets", "innodb_file_format", "innodb_large_prefix",
    ]
    for option in removed_renamed_options:
        print(option)

    print("Listing deprecated options:")
    deprecated_options = [
        "wsrep_replicate_myisam: Use wsrep_mode instead.",
        "wsrep_strict_ddl: Use wsrep_mode instead."
    ]
    for option in deprecated_options:
        print(option)
def upgrade_dependencies_10_6_to_10_11(hostname, username, password):
    print("Upgrading dependencies from 10.6 to 10.11")
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

            "Controls size of memory chunks allocated to the InnoDB buffer pool, now autosized for optimization.",
            "Sets behavior for auto-increment columns; ensuring reliability.",
            "Adjusts the batch reading strategy to enhance query performance under Spider engine.",
            "Manages batch processing for Spider engine operations, improving speed.",
            "Configures secondary batch read parameters for Spider to handle queries efficiently.",
            "Determines mode for batch key access hence optimizing indexing.",
            "Specifies how table names are processed in BKA, enabling better compatibility.",
            "Defines buffer size for Spider operations, crucial for handling large data transfers.",
            "Adjusts the bulk processing size for better handling of large payloads.",
            "Sets mode for bulk update operations to facilitate batch changes.",
            "Determines bulk update size for processing, enhancing batch update efficiency.",
            "Optimizes casual read performance for Spider queries.",
            "Adjusts timeout for connection attempts under Spider engine, enhancing reliability.",
            "Configures background mode for CRD operations, improving asynchronous tasks.",
            "Sets intervals for CRD processes, crucial for periodic updates.",
            "Establishes mode for CRD operations, optimizing consistency.",
            "Syncs CRD processes, ensuring data integrity.",
            "Determines the processing type for CRD, enhancing data tasks.",
            "Weights CRD procedure execution, allowing prioritization.",
            "Defines types for deleting rows in Spider, optimizing space management.",
            "Manages direct duplicate insert handling, reducing collision errors.",
            "Limits direct ordering, enhancing result handling.",
            "Sets error handling for read operations, ensuring robustness.",
            "Defines error handling mode for writes, ensuring reliability.",
            "Configures initial parameters for single read operations, improving efficiency.",
            "Specifies allocation size for SQL initialization, optimizing setup.",
            "Establishes limits for internal Spider operations, handling large results.",
            "Adjusts internal offset strategies for Spider, improving query handling.",
            "Optimizes internal Spider behaviors for better local execution.",
            "Helps optimize local data handling during Spider queries.",
            "Ensures CRD data is loaded at startup for prompt readiness.",
            "Ensures stateful data (STS) loads for Spider operations during startup.",
            "Improves memory efficiency for Spider reads, optimizing resource usage.",
            "Sets max order processing volume for Spider, high-performant configurations.",
            "Optimizes split reading processes in multi-node Spider setups.",
            "Determines network read timeout for Spider transactions, critical for reliability.",
            "Adjusts network write timeout settings under Spider, enhancing stability.",
            "Optimizes quick mode for transferring Spider data rapidly.",
            "Defines byte size for quick processing pages, customizing efficiency.",
            "Decides page size for Spider queries, optimizing storage.",
            "Configures read-only mode under Spider, restricting write operations.",
            "Resets SQL allocation, tailoring query resource usage.",
            "Controls secondary read setups for Spider, streamlining access.",
            "Adjusts locking strategies, maintaining data integrity.",
            "Optimizes semi-split reads, balancing resource utilization.",
            "Defines limit for semi-split tasks, optimizing splits.",
            "Manages lock connections for semi-table access, ensuring order.",
            "Adjusts locking strategies under Spider, promoting concurrency."
    ]


    for i, option in enumerate(options):
        print(f"Option: {option}")
        print(f"  Old Default: {old_defaults[i]}")
        print(f"  New Default: {new_defaults[i]}")
        print(f"  Description: {descriptions[i]}")


    removed_renamed_options = [
        "innodb_log_write_ahead_size: On Linux and Windows, the physical block size of the underlying storage is instead detected and used.",
        "innodb_version: Redundant.",
        "wsrep_replicate_myisam: Use wsrep_mode instead."
    ]
    print("Listing options that have been removed or renamed:")
    for option in removed_renamed_options:
        print(option)

    deprecated_options = [
        "keep_files_on_create: MariaDB now deletes orphan files, so this setting should never be necessary."
    ]
    print("Listing deprecated options:")
    for option in deprecated_options:
        print(option)
def main():
    hostname = input("Enter hostname: ")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    target_version = input("Enter target version: ")

    conn = connect_to_mariadb(hostname, username, password)
    current_version = get_mariadb_version(conn)
    
    print(f"Current MariaDB version: {current_version}")
    
    if current_version.startswith("10.4") and target_version == "10.11":
        upgrade_dependencies_10_4_to_10_5(hostname, username, password)
        upgrade_dependencies_10_5_to_10_6(hostname, username, password)
        upgrade_dependencies_10_6_to_10_11(hostname, username, password)
    elif current_version.startswith("10.5") and target_version == "10.11":
        upgrade_dependencies_10_5_to_10_6(hostname, username, password)
        upgrade_dependencies_10_6_to_10_11(hostname, username, password)

    conn.close()

if __name__ == "__main__":
    main()
