import questionary

import detector.WorkerDetector


def main():
    worker_detector = detector.WorkerDetector.WorkerDetector()

    print("Imported workers at start of run:\n{}".format(
        len(worker_detector.get_imported_workers())
    ))

    choices = worker_detector.get_unregistered_workers()
    if choices:
        workers_to_load = questionary.checkbox("All available workers:", choices=choices).ask()
        for worker in workers_to_load:
            worker_detector.import_worker(worker)
    else:
        print('Nothing to do here.')

    print("Imported workers at start of run:\n{}".format(
        len(worker_detector.get_imported_workers())
    ))
    print("Triggering print method of all workers:\n")
    worker_detector.trigger_message_from_imported_workers()

if __name__ == '__main__':
    main()
