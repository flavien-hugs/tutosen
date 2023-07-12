!function(){ 
    $('#earningTwo').length && (e = {
        series: [
        {
            name: 'Current Month',
            data: [
            10,
            20,
            15,
            25,
            18,
            28,
            22,
            32,
            24,
            34,
            26,
            38
            ]
        }
        ],
        labels: [
        'Jan',
        'Feb',
        'March',
        'April',
        'May',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
        'Oct',
        'Nov',
        'Dec'
        ],
        chart: {
            fontFamily: '$font-family-base',
            height: '280px',
            type: 'line',
            toolbar: {
                show: !1
            }
        },
        colors: [
        '#754FFE'
        ],
        stroke: {
            width: 4,
            curve: 'smooth',
            colors: [
            '#754FFE'
            ]
        },
        xaxis: {
            axisBorder: {
                show: !1
            },
            axisTicks: {
                show: !1
            },
            crosshairs: {
                show: !0
            },
            labels: {
                offsetX: 0,
                offsetY: 5,
                style: {
                    fontSize: '13px',
                    fontWeight: 400,
                    colors: '#a8a3b9'
                }
            }
        },
        yaxis: {
            labels: {
                formatter: function (e) {
                    return e + 'k'
                },
                style: {
                    fontSize: '13px',
                    fontWeight: 400,
                    colors: '#a8a3b9'
                },
                offsetX: - 15
            },
            tickAmount: 3,
            min: 10,
            max: 40
        },
        grid: {
            borderColor: '#e0e6ed',
            strokeDashArray: 5,
            xaxis: {
                lines: {
                    show: !1
                }
            },
            yaxis: {
                lines: {
                    show: !0
                }
            },
            padding: {
                top: 0,
                right: 0,
                bottom: 0,
                left: 0
            }
        },
        legend: {
            position: 'top',
            horizontalAlign: 'right',
            offsetY: - 50,
            fontSize: '16px',
            markers: {
                width: 10,
                height: 10,
                strokeWidth: 0,
                strokeColor: '#fff',
                fillColors: void 0,
                radius: 12,
                onClick: void 0,
                offsetX: 0,
                offsetY: 0
            },
            itemMargin: {
                horizontal: 0,
                vertical: 20
            }
        },
        tooltip: {
            theme: 'light',
            marker: {
                show: !0
            },
            x: {
                show: !1
            }
        },
        responsive: [
        {
            breakpoint: 575,
            options: {
                legend: {
                    offsetY: - 30
                }
            }
        }
        ]
    }, new ApexCharts(document.querySelector('#earningTwo'), e).render()),

    $('#traffic').length && (e = {
        dataLabels: {
            enabled: !1
        },
        series: [
            25,
            55,
            41
        ],
        labels: [
            'Courses',
            'Posts',
            'Comments'
        ],
        colors: [
            '#754FFE',
            '#CEC0FF',
            '#E8E2FF'
        ],
        chart: {
            width: 392,
            type: 'donut',
            zoom: { enabled: true }
        },
        plotOptions: {
            pie: {
                expandOnClick: !1,
                donut: {
                    size: '78%'
                }
            }
        },
        legend: {
            position: 'bottom',
            fontFamily: 'inter',
            fontWeight: 500,
            fontSize: '14px',
            markers: {
                width: 8,
                height: 8,
                strokeWidth: 0,
                strokeColor: '#fff',
                fillColors: void 0,
                radius: 12,
                customHTML: void 0,
                onClick: void 0,
                offsetX: 0,
                offsetY: 0
            },
            itemMargin: {
                horizontal: 8,
                vertical: 0
            }
        },
        tooltip: {
            theme: 'light',
            marker: {
                show: !0
            },
            x: {
                show: !1
            }
        },
        states: {
            hover: {
                filter: {
                    type: 'none'
                }
            }
        }
    }, new ApexCharts(document.querySelector('#traffic'), e).render()),

    $('#orderColumn').length && (e = {
        series: [
            {
                data: [
                    2,
                    6,
                    5,
                    3,
                    5,
                    6,
                    8,
                    9
                ]
            }
        ],
        chart: {
            toolbar: {
                show: !1
            },
            type: 'bar',
            height: 272
        },
        colors: [
        '#754FFE'
        ],
        plotOptions: {
            bar: {
                horizontal: !1,
                columnWidth: '12%',
                endingShape: 'rounded'
            }
        },
        dataLabels: {
            enabled: !1
        },
        stroke: {
            show: !0,
            width: 1,
            colors: [
            'transparent'
            ]
        },
        grid: {
            borderColor: '#e0e6ed',
            strokeDashArray: 5,
            xaxis: {
                lines: {
                    show: !1
                }
            }
        },
        xaxis: {
            categories: [
            '1 Jun',
            '9 Jun',
            '16 jun',
            '18 Jun',
            '19 Jun',
            '22 jun',
            '24 Jun',
            '26 Jun'
            ],
            axisBorder: {
                show: !1
            },
            labels: {
                offsetX: 0,
                offsetY: 5,
                style: {
                    fontSize: '13px',
                    fontWeight: 400,
                    colors: '#a8a3b9'
                }
            }
        },
        grid: {
            borderColor: '#e0e6ed',
            strokeDashArray: 5,
            xaxis: {
                lines: {
                    show: !1
                }
            },
            yaxis: {
                lines: {
                    show: !0
                }
            },
            padding: {
                top: 0,
                right: 0,
                bottom: 0,
                left: - 10
            }
        },
        yaxis: {
            title: {
                text: void 0
            },
            plotOptions: {
                bar: {
                    horizontal: !1,
                    endingShape: 'rounded',
                    columnWidth: '80%'
                }
            },
            labels: {
                style: {
                    fontSize: '13px',
                    fontWeight: 400,
                    colors: '#a8a3b9'
                },
                offsetX: - 10
            }
        },
        fill: {
            opacity: 1
        },
        tooltip: {
            y: {
                formatter: function (e) {
                    return e + ' sales '
                }
            },
            marker: {
                show: !0
            }
        }
    }, new ApexCharts(document.querySelector('#orderColumn'), e).render())
}();
