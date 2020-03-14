#!/usr/bin/env python3

# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.5.3 (default, Sep 14 2017, 22:58:41)
# [GCC 6.3.0 20170406]
# Embedded file name: PyoConnectMenu.py
# Compiled at: 2015-08-05 16:27:01
import os
import time
import importlib
# from PyoConnectLib import *
from myo_raw import MyoRaw
import numpy as np


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    try:
        import sklearn
        from joblib import load
        import keyboard
        import time
        import queue
        from multiprocessing import Queue
        from scripts import training
    except BaseException as e:
        logging.error("Failed to import Gesture script")
        logging.error(str(e))

    emg_queue = Queue(1)
    pose_map = {0: "Relaxed", 1: "Left", 2: "Right", 3: "Fist"}
    trainer = training.Trainer(pose_map.values(), emg_queue)
    model = None

    def on_emg(p, moving, times=[]):
        if not model:
            try:
                emg_queue.put(p, False)
            except queue.Full:
                pass
        else:
            y = model.predict(np.array([p]))
            logging.info("Classified " + pose_map[y[0]])
        # try:
        #     append_prediction(p)
        #     now = time.time()
        #     if predictions.count(p) >= threshold and (now - last_set) > 1:
        #         last_set = now
        #         return True
        #     else:
        #         return False
        # except Exception as e:
        #     print(e)
    myo = MyoRaw(None)
    myo.add_emg_handler(on_emg)
    myo.connect()
    trainer.start()

    try: 
        while True:
            t0 = time.time()
            p = myo.run(1.0)
            if not model and not trainer.is_alive():
                model = load("classifier.pkl")
    except KeyboardInterrupt:
        trainer.terminate()

# OpenConfig()
# LoadAllScripts()
# root = tk.Tk()
# root.title('PyoConnect v2.0')
# main = tk.Frame(root, width=300, height=300, background='gray95')
# main.pack(fill=tk.BOTH, expand=1)
# topframe = tk.Frame(main, width=300, height=50, padx=10, pady=10, background='gray20')
# topframe.pack_propagate(0)
# topframe.pack(fill=tk.BOTH)
# toplabel = tk.Label(topframe, text='PyoConnect', background='gray20', foreground='#50BBE7', font='Arial 20')
# toplabel.pack(fill=tk.BOTH)
# connframe = tk.Frame(main, width=300, height=50, padx=10, pady=10, background='gray95')
# connframe.pack(fill=tk.X)
# connbtn = tk.Button(connframe, text='Connect Myo', background='#50BBE7', foreground='white', border=0, command=ConnectMyo, relief=tk.RAISED)
# connbtn.pack(side=tk.LEFT)
# connbtn = tk.Button(connframe, text='Disconnect', background='#50BBE7', foreground='white', border=0, command=DisconnectMyo, relief=tk.RAISED)
# connbtn.pack(side=tk.RIGHT)
# btnframe = tk.Frame(main, width=280, padx=10, pady=10, background='gray95')
# btnframe.pack(fill=tk.X)
# i = 0
# btns = []
# for sfile in scriptlist:
#     si = scriptlist.index(sfile)
#     mname = sfile[:-3]
#     eframe = tk.Frame(btnframe, width=280, height='36', background='gray95', borderwidth='1', relief=tk.RIDGE)
#     eframe.pack_propagate(0)
#     eframe.pack(fill=tk.BOTH)
#     try:
#         etitle = modulelist[si].scriptTitle
#     except:
#         etitle = FormatFileName(sfile)

#     elabel = tk.Label(eframe, text=etitle, background='gray95')
#     elabel.pack(side=tk.LEFT)
#     ebtn = tk.Button(eframe, border=0)
#     btns.append(ebtn)
#     if mname in modulenamelist:
#         btns[i].config(text='ON', background='#50BBE7', relief=tk.SUNKEN, command=partial(SetOnOffScript, i))
#     else:
#         btns[i].config(text='off', background='gray95', relief=tk.RAISED, command=partial(SetOnOffScript, i))
#     btns[i].scriptname = sfile
#     btns[i].modname = mname
#     btns[i].script_id = i
#     btns[i].frame = eframe
#     btns[i].label = elabel
#     btns[i].pack(side=tk.RIGHT)
#     i += 1

# tk.Label(btnframe, text=' ', background='gray95').pack()
# tk.Button(btnframe, text='About', background='#50BBE7', border=0, command=AboutBox).pack(side=tk.LEFT)
# tk.Button(btnframe, text='Quit', background='#50BBE7', border=0, command=Close).pack(side=tk.RIGHT)
# pleaseQuit = False
# t0 = time.time()
# cnt = 0
# while pleaseQuit == False:
#     root.update()
#     if isMyoConnected:
#         t0 = time.time()
#         p = myo.run(1.0)
#         if time.time() - t0 > 0.3:
#             DisconnectMyo()
#         else:
#             myo.tick()

# try:
#     root.destroy()
# except:
#     pass
# # okay decompiling PyoManager.pyc
