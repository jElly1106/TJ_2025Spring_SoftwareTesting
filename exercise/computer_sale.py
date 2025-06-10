def calculate_commission(sales_amount):
    if sales_amount <= 1000:
        commission_rate = 0.10
    elif sales_amount <= 1800:
        commission_rate = 0.15
    else:
        commission_rate = 0.20
    return sales_amount * commission_rate

def main():
    # 产品定义
    host_price = 25
    display_price = 30
    peripheral_price = 45

    max_host_sales = 70
    max_display_sales = 80
    max_peripheral_sales = 90

    total_sales_amount = 0
    total_hosts_sold = 0
    total_displays_sold = 0
    total_peripherals_sold = 0

    print("电脑销售系统")
    print("输入 -1 作为主机销量以结束并计算总额。")

    while True:
        try:
            num_hosts_input = input("请输入本次销售的主机数量 (输入-1结束): ")
            if num_hosts_input == "-1":
                break
            
            num_hosts = int(num_hosts_input)
            num_displays = int(input("请输入本次销售的显示器数量: "))
            num_peripherals = int(input("请输入本次销售的外设数量: "))

            # 校验单次输入是否为非负数
            if num_hosts < 0 or num_displays < 0 or num_peripherals < 0:
                print("销售数量不能为负数，请重新输入。")
                continue

            # 校验累计销售数量是否超过上限
            if total_hosts_sold + num_hosts > max_host_sales:
                print(f"累计主机销售数量将超过上限 ({max_host_sales})，本次最多可销售 {max_host_sales - total_hosts_sold} 台主机。请重新输入。")
                continue
            if total_displays_sold + num_displays > max_display_sales:
                print(f"累计显示器销售数量将超过上限 ({max_display_sales})，本次最多可销售 {max_display_sales - total_displays_sold} 台显示器。请重新输入。")
                continue
            if total_peripherals_sold + num_peripherals > max_peripheral_sales:
                print(f"累计外设销售数量将超过上限 ({max_peripheral_sales})，本次最多可销售 {max_peripheral_sales - total_peripherals_sold} 台外设。请重新输入。")
                continue
            
            # 累加销售数量和销售额
            total_hosts_sold += num_hosts
            total_displays_sold += num_displays
            total_peripherals_sold += num_peripherals
            
            current_sales = (num_hosts * host_price) + \
                            (num_displays * display_price) + \
                            (num_peripherals * peripheral_price)
            total_sales_amount += current_sales
            print(f"本次录入销售额: {current_sales}元，已录入主机: {num_hosts}, 显示器: {num_displays}, 外设: {num_peripherals}")

        except ValueError:
            print("输入无效，请输入数字。")
        except Exception as e:
            print(f"发生错误: {e}")

    print("\n--- 月度销售统计 ---")
    print(f"本月销售总额: {total_sales_amount}元")
    print(f"本月销售主机总数: {total_hosts_sold}")
    print(f"本月销售显示器总数: {total_displays_sold}")
    print(f"本月销售外设总数: {total_peripherals_sold}")

    # 检查是否满足每月至少销售一台完整机器的条件
    if total_hosts_sold >= 1 and total_displays_sold >= 1 and total_peripherals_sold >= 1:
        if total_sales_amount > 0:
            commission = calculate_commission(total_sales_amount)
            print(f"本月佣金: {commission:.2f}元")
        else:
            # 理论上如果满足了各部件至少1个，销售额肯定大于0，但以防万一
            print("本月销售额为0，无佣金。")
    else:
        print("未满足每月至少销售一台完整机器（主机、显示器、外设各至少1件）的要求，无佣金。")

if __name__ == "__main__":
    main()