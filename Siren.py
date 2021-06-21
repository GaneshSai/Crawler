from new_crawler import *
from bert import main_bert
from Data_CSV import main_csv
from multiprocessing import Process
from time import sleep

main()
main_csv()
main_bert()

if __name__ == "__main__":
    p1 = Process(target=main())
    p1.start()
    p2 = Process(target=main_csv())
    p2.start()
    sleep(5)
    p3 = Process(target=main_bert())
    p3.start()
    p1.join()
    p2.join()
    p3.join()
