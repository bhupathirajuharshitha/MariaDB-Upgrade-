#!/bin/bash

# Function to prompt and read inputs without echoing password
read_db_credentials() {
  echo -n "Enter MariaDB Hostname: "
  read HOSTNAME

  echo -n "Enter MariaDB Username: "
  read USERNAME

  echo -n "Enter MariaDB Password: "
  read -s PASSWORD
  echo
}

# Check configuration for changed default values
check_changed_defaults() {
  echo "Checking options with changed default values..."

  MYSQL_CMD="mysql -h $HOSTNAME -u $USERNAME -p$PASSWORD -e"

  OPTIONS=(
    "innodb_adaptive_hash_index"
    "innodb_checksum_algorithm"
    "innodb_log_optimize_ddl"
    "slave_parallel_mode"
    "performance_schema_max_cond_classes"
    "performance_schema_max_file_classes"
    "performance_schema_max_mutex_classes"
    "performance_schema_max_rwlock_classes"
    "performance_schema_setup_actors_size"
    "performance_schema_setup_objects_size"
  )

  NEW_DEFAULTS=(
    "OFF"
    "full_crc32"
    "OFF"
    "optimistic"
    "90"
    "80"
    "210"
    "50"
    "-1"
    "-1"
  )

  DESCRIPTIONS=(
    "Controls the use of the adaptive hash index, reducing potential overhead."
    "Switches to a more comprehensive checksum algorithm."
    "Disables optimization in the logging of DDL statements."
    "Changes parallel slave execution mode to a more aggressive approach."
    "Increases the number of condition classes available in the performance schema."
    "Expands the number of file classes for performance monitoring."
    "Boosts the count of mutex classes in performance data collection."
    "Enhances the tracking of read-write lock classes in the performance schema."
    "Sets the setup actors size, if not explicitly defined, to unlimited."
    "Defines setup objects size to unlimited, optimizing storage."
  )

  for i in "${!OPTIONS[@]}"; do
    CURRENT_VALUE=$($MYSQL_CMD "SHOW VARIABLES LIKE '${OPTIONS[i]}'" | grep "${OPTIONS[i]}" | awk '{print $2}')
    echo "${OPTIONS[i]}: Current Value: $CURRENT_VALUE, New Default: ${NEW_DEFAULTS[i]}"
    echo "Description: ${DESCRIPTIONS[i]}"
  done
}

# List deprecated options
list_deprecated_options() {
  echo "Listing deprecated options and their reasons..."

  DEPRECATED_OPTIONS=(
    "innodb_adaptive_max_sleep_delay: No need for thread throttling anymore."
    "innodb_background_scrub_data_check_interval: Problematic ‘background scrubbing’ code removed."
    "innodb_background_scrub_data_interval: Problematic ‘background scrubbing’ code removed."
    "innodb_background_scrub_data_compressed: Problematic ‘background scrubbing’ code removed."
    "innodb_background_scrub_data_uncompressed: Problematic ‘background scrubbing’ code removed."
    "innodb_buffer_pool_instances: Having more than one buffer pool is no longer necessary."
    "innodb_commit_concurrency: No need for thread throttling any more."
    "innodb_concurrency_tickets: No need for thread throttling any more."
    "innodb_log_files_in_group: Redo log was unnecessarily split into multiple files. Limited to 1 from MariaDB 10.5."
    "innodb_log_optimize_ddl: Prohibited optimizations."
    "innodb_page_cleaners: Having more than one page cleaner task no longer necessary."
    "innodb_replication_delay: No need for thread throttling any more."
    "innodb_scrub_log: Never really worked as intended, redo log format is being redone."
    "innodb_scrub_log_speed: Never really worked as intended, redo log format is being redone."
    "innodb_thread_concurrency: No need for thread throttling any more."
    "innodb_thread_sleep_delay: No need for thread throttling any more."
    "innodb_undo_logs: It always makes sense to use the maximum number of rollback segments."
    "large_page_size: Unused since multiple page size support was added."
  )

  for option in "${DEPRECATED_OPTIONS[@]}"; do
    echo "$option"
  done
}

# Main script execution
read_db_credentials
check_changed_defaults
list_deprecated_options
