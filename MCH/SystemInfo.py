import psutil, time, sys, platform as pf, x86cpu
from tkinter import *
def system_info():
    xi = x86cpu.info
    if __name__ == '__main__':
        t = Tk()
    else:
        t = Toplevel()
    t.wm_attributes('-topmost', 1)
    t.resizable(0, 0)
    t.title('欢迎 ' + str(psutil.users()[0].name) + ' 使用系统信息显示重置版 V2.0')
    v1 = StringVar()
    v2 = StringVar()
    v3 = StringVar()
    v4 = StringVar()
    v5 = StringVar()
    l1 = Label(t, textvariable = v1)
    l2 = Label(t, textvariable = v2)
    l3 = Label(t, textvariable = v3)
    l4 = Label(t, textvariable = v4)
    l5 = Label(t, textvariable = v5)
    l6 = Label(t, text = '-----硬件信息-----')
    # gwv = sys.getwindowsversion()
    # l7 = Label(t, text = '系统: Windows {}.{} Build {}{}'.format(gwv.major, gwv.minor, gwv.build, ' SP ' + gmv.service_pack if gwv.service_pack else ''))
    # l8 = Label(t, text = 'CPU: {} {}'.format(xi.vendor, xi.brand))
    l7 = Label(t, text = '计算机名: ' + pf.node() + ', 系统: ' + pf.platform() + '\n'
                + '处理器: ' + pf.processor() + '\n' + xi.brand)
    l1.pack()
    l2.pack()
    l3.pack()
    l4.pack()
    l5.pack()
    l6.pack()
    l7.pack()
    # ----- CPU -----
    def get_cpu():
        cpu_percent = psutil.cpu_percent(interval = 0.5)
        cpu_percent_per = psutil.cpu_percent(interval = 0.5, percpu = 1)
        for i in range(len(cpu_percent_per)):
            cpu_percent_per[i] = str(cpu_percent_per[i])
        ps = len(psutil.pids())
        return cpu_percent, cpu_percent_per, ps
    # ----- Memory -----
    def get_mem():
        memory = psutil.virtual_memory()
        return memory
    # ----- Battery -----
    def get_batt():
        battery = psutil.sensors_battery()
        left = battery.secsleft
        plugged = battery.power_plugged
        percent = str(battery.percent)
        if left == 4294967295:
            left = '正在获取...'
        if not plugged:
            plugged = '未充电'
        else:
            plugged = '正在充电'
        return left, plugged, percent
    # ----- Misc -----
    def get_misc():
        bt = psutil.boot_time()
        now = time.time()
        tm = round(now - bt)
        s = tm % 60
        m = tm // 60 % 60
        h = tm // 3600
        return h, m, s
    # ----- Time -----
    def get_time():
        now = time.strftime('%Y-%m-%d %H:%M:%S | %A', time.localtime())
        return '当前时间 ' + now
    while 1:
        cpu_percent, cpu_percent_per, ps = get_cpu()
        memory = get_mem()
        left, plugged, percent = get_batt()
        h, m, s = get_misc()
        cpu_str = 'CPU使用率 ' + str(cpu_percent) + '% (' + str('%, '.join(cpu_percent_per)) + '%) ' + ' | 进程数 ' + str(ps)
        mem_str = '内存使用 ' + str(round(memory.used / 1024 / 1024, 2)) + ' MB/' + str(round(memory.total / 1024 / 1024, 2)) \
        + ' MB | ' + str(memory.percent) + '%'
        try:
            batt_str = '电量 ' + percent + '% ' + str(left.POWER_TIME_UNLIMITED) + ' | ' + plugged
        except:
            if isinstance(left, int):
                ss = left % 60
                mm = left // 60 % 60
                hh = left // 3600
                tms = str(hh) + '时' + '0' * (mm < 10) + str(mm) + '分' + '0' * (ss < 10) + str(ss) + '秒'
                batt_str = '电量 ' + percent + '% 可用时间 ' + tms + ' (需15秒左右时间更新，请等待)'
            else:
                batt_str = '电量 ' + percent + '% 可用时间 ' + left + ' (需15秒左右时间更新，请等待)'
        else:
            batt_str = '电量 ' + percent + '% ' + plugged
        misc_str = '已开机 ' + str(h) + '时' + '0' * (m < 10) + str(m) + '分' + '0' * (s < 10) + str(s) + '秒'
        time_str = get_time()
        v1.set(cpu_str)
        v2.set(mem_str)
        v3.set(batt_str)
        v4.set(misc_str)
        v5.set(time_str)
        t.update()
if __name__ == '__main__':
    system_info()
